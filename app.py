from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import random
from flasgger import Swagger  # Импортируем Swagger

app = Flask(__name__)
Swagger(app)  # Инициализируем Swagger

app.secret_key = 'your_secret_key'

# Главная страница с поиском
@app.route('/')
def index():
    """
    Главная страница с выбором случайных книг
    ---
    responses:
      200:
        description: Отображает список случайных книг
        content:
          application/json:
            example:
              books: [ "Book 1", "Book 2", "Book 3"]
    """
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title, author FROM books")
    all_books = cursor.fetchall()
    conn.close()
    
    # Выбираем 10 случайных книг
    random_books = random.sample(all_books, min(len(all_books), 10))  # Если книг меньше 10, выбираем все
    return render_template('index.html', random_books=random_books)

# Путь для обработки запроса на поиск книг
@app.route('/search', methods=['POST'])
def search_books():
    """
    Поиск книг по названию или автору
    ---
    parameters:
      - name: search_term
        in: formData
        type: string
        required: true
        description: Строка для поиска книг
    responses:
      200:
        description: Возвращает список книг, соответствующих запросу
        content:
          application/json:
            example:
              books: [
                {"id": 1, "title": "Book 1", "author": "Author 1", "amount": 10},
                {"id": 2, "title": "Book 2", "author": "Author 2", "amount": 5}
              ]
    """
    search_term = request.form['search_term']
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            id, 
            title, 
            author, 
            amount
        FROM books
        WHERE (title LIKE ? OR author LIKE ?)
        AND amount > 0
        ORDER BY id ASC
    """, ('%' + search_term + '%', '%' + search_term + '%'))
    books = cursor.fetchall()
    conn.close()

    return render_template('search_results.html', books=books)

# Путь для добавления книги в корзину
@app.route('/add_to_cart/<int:book_id>', methods=['POST'])
def add_to_cart(book_id):
    """
    Добавление книги в корзину
    ---
    parameters:
      - name: book_id
        in: path
        type: integer
        required: true
        description: Идентификатор книги
      - name: quantity
        in: formData
        type: integer
        default: 1
        description: Количество добавляемых книг
    responses:
      200:
        description: Книга добавлена в корзину
        content:
          application/json:
            example:
              message: "Book added to cart!"
    """
    quantity = int(request.form.get('quantity', 1))  # Получаем количество из формы
    if 'cart' not in session:
        session['cart'] = {}

    # Проверяем, есть ли уже эта книга в корзине, и увеличиваем количество
    if str(book_id) in session['cart']:
        session['cart'][str(book_id)] += quantity
    else:
        session['cart'][str(book_id)] = quantity

    session.modified = True
    return "Book added to cart!"  # Возвращаем сообщение, которое будет отображено на странице

# Путь для удаления книги из корзины
@app.route('/remove_from_cart/<int:book_id>', methods=['GET', 'POST'])
def remove_from_cart(book_id):
    """
    Удаление книги из корзины
    ---
    parameters:
      - name: book_id
        in: path
        type: integer
        required: true
        description: Идентификатор книги для удаления
    responses:
      200:
        description: Книга удалена из корзины
        content:
          application/json:
            example:
              message: "Book removed from cart!"
    """
    if 'cart' in session:
        if str(book_id) in session['cart']:
            del session['cart'][str(book_id)]  # Удаляем книгу из корзины
            session.modified = True
    return redirect(url_for('cart', message="Book removed from cart!"))

# Путь для отображения корзины
@app.route('/cart')
def cart():
    """
    Отображение корзины
    ---
    responses:
      200:
        description: Показать книги в корзине
        content:
          application/json:
            example:
              cart: [
                {"id": 1, "title": "Book 1", "author": "Author 1", "quantity": 2}
              ]
    """
    message = request.args.get('message', '')
    if 'cart' in session and len(session['cart']) > 0:
        cart_books = session['cart']
        conn = sqlite3.connect('books.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE id IN ({})".format(','.join('?' for _ in cart_books)), tuple(cart_books.keys()))
        books_in_cart = cursor.fetchall()
        conn.close()

        # Добавляем количество каждой книги из корзины
        books_with_quantity = [
            {**dict(zip([desc[0] for desc in cursor.description], book)), "quantity": cart_books[str(book[0])] }
            for book in books_in_cart
        ]
    else:
        books_with_quantity = []

    return render_template('cart.html', books=books_with_quantity, message=message)

# Путь для оформления заказа
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """
    Оформление заказа
    ---
    responses:
      200:
        description: Оформить заказ и уменьшить количество книг на складе
    """
    if 'cart' in session and session['cart']:
        cart_books = session['cart']
        conn = sqlite3.connect('books.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE id IN ({})".format(','.join('?' for _ in cart_books)), tuple(cart_books.keys()))
        books_in_cart = cursor.fetchall()

        books_with_quantity = [
            {**dict(zip([desc[0] for desc in cursor.description], book)), "quantity": cart_books[str(book[0])] }
            for book in books_in_cart
        ]

        if request.method == 'POST':
            # Проверяем и уменьшаем количество книг
            for book_id, quantity in cart_books.items():
                cursor.execute("SELECT amount FROM books WHERE id = ?", (book_id,))
                amount = cursor.fetchone()
                if amount and amount[0] >= quantity:
                    cursor.execute("UPDATE books SET amount = amount - ? WHERE id = ?", (quantity, book_id))
                else:
                    return render_template('checkout.html', books=books_with_quantity, message="Some books are out of stock.")

            conn.commit()
            conn.close()

            session.pop('cart', None)
            return render_template('checkout_success.html', books=books_in_cart)
        
        conn.close()
        return render_template('checkout.html', books=books_with_quantity)
    else:
        return render_template('cart.html', books=[], message="Your cart is empty. Please add some books.")

if __name__ == '__main__':
    app.run(debug=True)
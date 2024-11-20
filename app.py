from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import random

app = Flask(__name__)

# Устанавливаем секретный ключ для сессий
app.secret_key = 'your_secret_key'

# Путь для главной страницы с поиском
@app.route('/')
def index():
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
    search_term = request.form['search_term']
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    # Обновляем запрос для выборки только первой записи книги
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
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(book_id)
    session.modified = True
    return redirect(url_for('cart', message="Book added to cart!"))

# Путь для удаления книги из корзины
@app.route('/remove_from_cart/<int:book_id>', methods=['GET', 'POST'])
def remove_from_cart(book_id):
    if 'cart' in session:
        if book_id in session['cart']:
            session['cart'].remove(book_id)
            session.modified = True
    return redirect(url_for('cart', message="Book removed from cart!"))

# Путь для отображения корзины
@app.route('/cart')
def cart():
    message = request.args.get('message', '')
    if 'cart' in session and len(session['cart']) > 0:
        cart_books = session['cart']
        conn = sqlite3.connect('books.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE id IN ({})".format(','.join('?' for _ in cart_books)), tuple(cart_books))
        books_in_cart = cursor.fetchall()
        conn.close()
    else:
        books_in_cart = []
    return render_template('cart.html', books=books_in_cart, message=message)

# Путь для оформления заказа
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'cart' in session and session['cart']:
        cart_books = session['cart']
        conn = sqlite3.connect('books.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE id IN ({})".format(','.join('?' for _ in cart_books)), tuple(cart_books))
        books_in_cart = cursor.fetchall()

        if request.method == 'POST':
            # Уменьшаем количество книг в базе данных
            for book_id in cart_books:
                cursor.execute("SELECT amount FROM books WHERE id = ?", (book_id,))
                amount = cursor.fetchone()
                if amount and amount[0] > 0:
                    cursor.execute("UPDATE books SET amount = amount - 1 WHERE id = ?", (book_id,))
                else:
                    return render_template('checkout.html', books=books_in_cart, message="Some books are out of stock.")

            conn.commit()  # Сохраняем изменения в базе данных
            conn.close()

            session.pop('cart', None)  # Очищаем корзину
            return render_template('checkout_success.html', books=books_in_cart)
        
        conn.close()
        return render_template('checkout.html', books=books_in_cart)
    else:
        return render_template('cart.html', books=[], message="Your cart is empty. Please add some books.")

if __name__ == '__main__':
    app.run(debug=True)
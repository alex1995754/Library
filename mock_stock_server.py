from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

# Путь для получения количества книги на складе
@app.route('/stock/<int:book_id>', methods=['GET'])
def check_stock(book_id):
    # Проверяем количество книги на складе
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute("SELECT stock FROM books WHERE id = ?", (book_id,))
    stock = cursor.fetchone()
    conn.close()
    
    if stock:
        return jsonify({"book_id": book_id, "stock": stock[0]})
    else:
        return jsonify({"error": "Book not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Работает на другом порту
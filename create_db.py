import sqlite3
import random

# Список реальных книг и авторов для примера
books_data = [
     ('The Catcher in the Rye', 'J.D. Salinger'),
    ('To Kill a Mockingbird', 'Harper Lee'),
    ('1984', 'George Orwell'),
    ('The Great Gatsby', 'F. Scott Fitzgerald'),
    ('The Hobbit', 'J.R.R. Tolkien'),
    ('Moby-Dick', 'Herman Melville'),
    ('Pride and Prejudice', 'Jane Austen'),
    ('The Lord of the Rings', 'J.R.R. Tolkien'),
    ('War and Peace', 'Leo Tolstoy'),
    ('Crime and Punishment', 'Fyodor Dostoevsky'),
    ('Brave New World', 'Aldous Huxley'),
    ('The Picture of Dorian Gray', 'Oscar Wilde'),
    ('Animal Farm', 'George Orwell'),
    ('Wuthering Heights', 'Emily Brontë'),
    ('Jane Eyre', 'Charlotte Brontë'),
    ('Les Misérables', 'Victor Hugo'),
    ('The Odyssey', 'Homer'),
    ('The Iliad', 'Homer'),
    ('Dracula', 'Bram Stoker'),
    ('The Catcher in the Rye', 'J.D. Salinger'),
    ('The Shining', 'Stephen King'),
    ('Harry Potter and the Sorcerer\'s Stone', 'J.K. Rowling'),
    ('The Chronicles of Narnia', 'C.S. Lewis'),
    ('The Da Vinci Code', 'Dan Brown'),
    ('The Alchemist', 'Paulo Coelho'),
    ('The Book Thief', 'Markus Zusak'),
    ('The Fault in Our Stars', 'John Green'),
    ('Gone with the Wind', 'Margaret Mitchell'),
    ('The Hobbit', 'J.R.R. Tolkien'),
    ('Fahrenheit 451', 'Ray Bradbury'),
    ('The Secret Garden', 'Frances Hodgson Burnett'),
    ('The Grapes of Wrath', 'John Steinbeck'),
    ('The Outsiders', 'S.E. Hinton'),
    ('The Call of the Wild', 'Jack London'),
    ('The Road', 'Cormac McCarthy'),
    ('The Girl with the Dragon Tattoo', 'Stieg Larsson'),
    ('The Hitchhiker\'s Guide to the Galaxy', 'Douglas Adams'),
    ('Little Women', 'Louisa May Alcott'),
    ('The Great Gatsby', 'F. Scott Fitzgerald'),
    ('Ender\'s Game', 'Orson Scott Card'),
    ('The Help', 'Kathryn Stockett'),
    ('The Hunger Games', 'Suzanne Collins'),
    ('A Game of Thrones', 'George R.R. Martin'),
    ('Catch-22', 'Joseph Heller'),
    ('The Kite Runner', 'Khaled Hosseini'),
    ('The Lord of the Rings: The Fellowship of the Ring', 'J.R.R. Tolkien'),
    ('The Handmaid\'s Tale', 'Margaret Atwood'),
    ('Pride and Prejudice', 'Jane Austen'),
    ('The Sun Also Rises', 'Ernest Hemingway'),
    ('Of Mice and Men', 'John Steinbeck'),
    ('The Scarlet Letter', 'Nathaniel Hawthorne'),
    ('Frankenstein', 'Mary Shelley'),
    ('The Bell Jar', 'Sylvia Plath'),
    ('The Silence of the Lambs', 'Thomas Harris'),
    ('The Girl on the Train', 'Paula Hawkins'),
    ('The Night Circus', 'Erin Morgenstern'),
    ('A Tale of Two Cities', 'Charles Dickens'),
    ('The Art of War', 'Sun Tzu'),
    ('The Princess Bride', 'William Goldman'),
    ('The Hunger Games: Catching Fire', 'Suzanne Collins'),
    ('The Outsiders', 'S.E. Hinton'),
    ('The Girl with the Dragon Tattoo', 'Stieg Larsson'),
    ('A Wrinkle in Time', 'Madeleine L\'Engle'),
    ('Slaughterhouse-Five', 'Kurt Vonnegut'),
    ('The Color Purple', 'Alice Walker'),
    ('Dr. Jekyll and Mr. Hyde', 'Robert Louis Stevenson'),
    ('The Secret History', 'Donna Tartt'),
    ('The 5th Wave', 'Rick Yancey'),
    ('The Time Traveler\'s Wife', 'Audrey Niffenegger'),
    ('Shogun', 'James Clavell'),
    ('The Shadow of the Wind', 'Carlos Ruiz Zafón'),
    ('The Thirteenth Tale', 'Diane Setterfield'),
    ('The Book Thief', 'Markus Zusak'),
    ('The Road', 'Cormac McCarthy'),
    ('The Maze Runner', 'James Dashner'),
    ('Dune', 'Frank Herbert'),
    ('The Night Manager', 'John le Carré'),
    ('The Three-Body Problem', 'Liu Cixin'),
    ('Ready Player One', 'Ernest Cline'),
    ('The Martian', 'Andy Weir'),
    ('The Secret Garden', 'Frances Hodgson Burnett'),
    ('The Shadow of the Wind', 'Carlos Ruiz Zafón'),
    ('Memoirs of a Geisha', 'Arthur Golden'),
    ('The Book of M', 'Peng Shepherd'),
    ('The Help', 'Kathryn Stockett'),
    ('The Brothers Karamazov', 'Fyodor Dostoevsky'),
    ('1984', 'George Orwell'),
    ('The Time Machine', 'H.G. Wells'),
    ('Wicked', 'Gregory Maguire'),
    ('The Count of Monte Cristo', 'Alexandre Dumas'),
    ('The Alchemist', 'Paulo Coelho'),
    ('The Fountainhead', 'Ayn Rand'),
    ('Atlas Shrugged', 'Ayn Rand'),
    ('The Hobbit', 'J.R.R. Tolkien'),
    ('The Nightingale', 'Kristin Hannah'),
    ('The Sorrows of Young Werther', 'Johann Wolfgang von Goethe'),
    ('The Catcher in the Rye', 'J.D. Salinger'),
    ('Lord of the Flies', 'William Golding'),
    ('The Great Alone', 'Kristin Hannah'),
    ('The Girl on the Train', 'Paula Hawkins'),
    ('Gone Girl', 'Gillian Flynn'),
    ('The Handmaid\'s Tale', 'Margaret Atwood'),
    ('Where the Crawdads Sing', 'Delia Owens'),
    ('The Light Between Oceans', 'M.L. Stedman'),
    ('The Silent Patient', 'Alex Michaelides')
    # Дополните список до 100 книг
]

# Функция для создания базы данных и таблицы
def create_books_db():
    # Подключаемся к базе данных (если файл существует, он будет открыт, если нет — создан)
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    # Создаём таблицу books с тремя колонками
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            amount INTEGER NOT NULL
        )
    ''')

    # Вставляем 100 книг с случайным количеством
    for _ in range(100):
        book = random.choice(books_data)  # Выбираем случайную книгу из списка
        amount = random.randint(1, 50)  # Генерируем случайное количество от 1 до 50
        cursor.execute('''
            INSERT INTO books (title, author, amount)
            VALUES (?, ?, ?)
        ''', (book[0], book[1], amount))

    # Сохраняем изменения
    conn.commit()

    # Закрываем соединение с базой данных
    conn.close()

    print("Database created and populated with 100 books.")

# Запускаем функцию создания базы данных
create_books_db()

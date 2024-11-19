import sqlite3
import random

# Базовый список книг с известными названиями и авторами
books_data = [
    ("To Kill a Mockingbird", "Harper Lee"),
    ("1984", "George Orwell"),
    ("The Great Gatsby", "F. Scott Fitzgerald"),
    ("Pride and Prejudice", "Jane Austen"),
    ("The Catcher in the Rye", "J.D. Salinger"),
    ("The Lord of the Rings", "J.R.R. Tolkien"),
    ("The Hobbit", "J.R.R. Tolkien"),
    ("Fahrenheit 451", "Ray Bradbury"),
    ("Jane Eyre", "Charlotte Bronte"),
    ("Wuthering Heights", "Emily Bronte"),
    ("Brave New World", "Aldous Huxley"),
    ("Moby Dick", "Herman Melville"),
    ("War and Peace", "Leo Tolstoy"),
    ("Crime and Punishment", "Fyodor Dostoevsky"),
    ("The Brothers Karamazov", "Fyodor Dostoevsky"),
    ("Anna Karenina", "Leo Tolstoy"),
    ("Great Expectations", "Charles Dickens"),
    ("Oliver Twist", "Charles Dickens"),
    ("David Copperfield", "Charles Dickens"),
    ("Les Misérables", "Victor Hugo"),
    ("The Count of Monte Cristo", "Alexandre Dumas"),
    ("The Three Musketeers", "Alexandre Dumas"),
    ("Don Quixote", "Miguel de Cervantes"),
    ("The Picture of Dorian Gray", "Oscar Wilde"),
    ("Dracula", "Bram Stoker"),
    ("Frankenstein", "Mary Shelley"),
    ("The Adventures of Sherlock Holmes", "Arthur Conan Doyle"),
    ("A Study in Scarlet", "Arthur Conan Doyle"),
    ("The Hound of the Baskervilles", "Arthur Conan Doyle"),
    ("Alice's Adventures in Wonderland", "Lewis Carroll"),
    ("Through the Looking-Glass", "Lewis Carroll"),
    ("The Wind in the Willows", "Kenneth Grahame"),
    ("Treasure Island", "Robert Louis Stevenson"),
    ("Strange Case of Dr Jekyll and Mr Hyde", "Robert Louis Stevenson"),
    ("Gulliver's Travels", "Jonathan Swift"),
    ("Robinson Crusoe", "Daniel Defoe"),
    ("The Odyssey", "Homer"),
    ("The Iliad", "Homer"),
    ("Hamlet", "William Shakespeare"),
    ("Macbeth", "William Shakespeare"),
    ("Romeo and Juliet", "William Shakespeare"),
    ("The Tempest", "William Shakespeare"),
    ("A Tale of Two Cities", "Charles Dickens"),
    ("Sense and Sensibility", "Jane Austen"),
    ("Persuasion", "Jane Austen"),
    ("Northanger Abbey", "Jane Austen"),
    ("The Grapes of Wrath", "John Steinbeck"),
    ("Of Mice and Men", "John Steinbeck"),
    ("East of Eden", "John Steinbeck"),
    ("The Pearl", "John Steinbeck"),
    ("Cannery Row", "John Steinbeck"),
    ("Animal Farm", "George Orwell"),
    ("Lord of the Flies", "William Golding"),
    ("The Old Man and the Sea", "Ernest Hemingway"),
    ("For Whom the Bell Tolls", "Ernest Hemingway"),
    ("A Farewell to Arms", "Ernest Hemingway"),
    ("The Sun Also Rises", "Ernest Hemingway"),
    ("Slaughterhouse-Five", "Kurt Vonnegut"),
    ("Catch-22", "Joseph Heller"),
    ("On the Road", "Jack Kerouac"),
    ("Beloved", "Toni Morrison"),
    ("Song of Solomon", "Toni Morrison"),
    ("The Bluest Eye", "Toni Morrison"),
    ("Gone with the Wind", "Margaret Mitchell"),
    ("The Book Thief", "Markus Zusak"),
    ("The Road", "Cormac McCarthy"),
    ("No Country for Old Men", "Cormac McCarthy"),
    ("Blood Meridian", "Cormac McCarthy"),
    ("The Alchemist", "Paulo Coelho"),
    ("Veronika Decides to Die", "Paulo Coelho"),
    ("Eleven Minutes", "Paulo Coelho"),
    ("The Pilgrimage", "Paulo Coelho"),
    ("The Kite Runner", "Khaled Hosseini"),
    ("A Thousand Splendid Suns", "Khaled Hosseini"),
    ("And the Mountains Echoed", "Khaled Hosseini"),
    ("Life of Pi", "Yann Martel"),
    ("The Hunger Games", "Suzanne Collins"),
    ("Catching Fire", "Suzanne Collins"),
    ("Mockingjay", "Suzanne Collins"),
    ("The Fault in Our Stars", "John Green"),
    ("Looking for Alaska", "John Green"),
    ("Paper Towns", "John Green"),
    ("An Abundance of Katherines", "John Green"),
    ("Divergent", "Veronica Roth"),
    ("Insurgent", "Veronica Roth"),
    ("Allegiant", "Veronica Roth"),
    ("Carve the Mark", "Veronica Roth"),
    ("The Maze Runner", "James Dashner"),
    ("The Scorch Trials", "James Dashner"),
    ("The Death Cure", "James Dashner"),
    ("The Kill Order", "James Dashner")
]

# Если книг меньше 100, добавляем дополнительные записи
while len(books_data) < 100:
    books_data.append((f"Book {len(books_data)+1}", f"Author {len(books_data)+1}"))

# Создаем подключение к базе данных
conn = sqlite3.connect("books.db")
cursor = conn.cursor()

# Создаем таблицу books
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    amount INTEGER NOT NULL
)
""")

# Добавляем книги в базу данных
random.shuffle(books_data)  # Перемешиваем список
books = [(title, author, random.randint(20, 100)) for title, author in books_data[:100]]

# Вставляем данные в таблицу
cursor.executemany("INSERT INTO books (title, author, amount) VALUES (?, ?, ?)", books)

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()

print("База данных books.db успешно создана и заполнена 100 уникальными книгами.")
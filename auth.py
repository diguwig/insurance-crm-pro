import sqlite3
import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def init_db():
    conn = sqlite3.connect('insurance.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (username TEXT PRIMARY KEY, password TEXT, role TEXT)''')

    # Обновленная таблица клиентов
    cursor.execute('''CREATE TABLE IF NOT EXISTS clients 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       name TEXT, 
                       policy TEXT, 
                       address TEXT,
                       phone TEXT,
                       email TEXT,
                       level TEXT,
                       start_date TEXT,
                       end_date TEXT)''')

    users = [('admin', hash_password('admin123'), 'a'),
             ('user', hash_password('user123'), 'u')]
    cursor.executemany("INSERT OR IGNORE INTO users VALUES (?, ?, ?)", users)
    conn.commit()
    conn.close()


def check_login(username, password):
    conn = sqlite3.connect('insurance.db')
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username=? AND password=?",
                   (username, hash_password(password)))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

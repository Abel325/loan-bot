import sqlite3
from config import DATABASE_NAME


def connect_db():
    return sqlite3.connect(DATABASE_NAME)


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,
        full_name TEXT,
        national_id TEXT,
        phone_number TEXT,
        mobile_money TEXT,
        employment_status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Loan applications table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS loans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER,
        loan_purpose TEXT,
        loan_amount INTEGER,
        status TEXT DEFAULT 'Pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_user(telegram_id, full_name, national_id, phone_number, mobile_money, employment_status):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO users
    (telegram_id, full_name, national_id, phone_number, mobile_money, employment_status)
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (
        telegram_id,
        full_name,
        national_id,
        phone_number,
        mobile_money,
        employment_status
    ))

    conn.commit()
    conn.close()


def get_user(telegram_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE telegram_id=?",
        (telegram_id,)
    )

    user = cursor.fetchone()

    conn.close()

    return user


def save_loan(telegram_id, loan_purpose, loan_amount):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO loans
    (telegram_id, loan_purpose, loan_amount)
    VALUES (?, ?, ?)
    """,
    (
        telegram_id,
        loan_purpose,
        loan_amount
    ))

    conn.commit()
    conn.close()


def get_loans(telegram_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM loans WHERE telegram_id=?",
        (telegram_id,)
    )

    loans = cursor.fetchall()

    conn.close()

    return loans

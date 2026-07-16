import sqlite3
import random
from datetime import datetime, timedelta


DATABASE = "database.db"



# ================= CREATE DATABASE =================

def create_database():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()



    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_id INTEGER UNIQUE,

        full_name TEXT,

        national_id TEXT,

        phone_number TEXT,

        mobile_money TEXT,

        employment_status TEXT,

        verified TEXT DEFAULT 'No'

    )
    """)



    cursor.execute("""
    CREATE TABLE IF NOT EXISTS loans(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_id INTEGER,

        purpose TEXT,

        amount REAL,

        status TEXT DEFAULT 'Pending',

        decision_note TEXT,

        decision_date TEXT,

        interest_rate REAL DEFAULT 0,

        interest_amount REAL DEFAULT 0,

        total_repayment REAL DEFAULT 0,

        repayment_period INTEGER DEFAULT 0,

        monthly_payment REAL DEFAULT 0,

        remaining_balance REAL DEFAULT 0,

        next_payment_date TEXT,

        payment_status TEXT DEFAULT 'Pending',

        disbursement_status TEXT DEFAULT 'Not Disbursed'

    )
    """)



    cursor.execute("""
    CREATE TABLE IF NOT EXISTS otp(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_id INTEGER,

        otp TEXT,

        created_at TEXT

    )
    """)



    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_id INTEGER,

        loan_id INTEGER,

        amount REAL,

        payment_date TEXT,

        status TEXT DEFAULT 'Completed'

    )
    """)



    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin_logs(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        admin_id INTEGER,

        action TEXT,

        loan_id INTEGER,

        created_at TEXT

    )
    """)



    conn.commit()

    conn.close()





# ================= SAVE USER =================

def save_user(
    telegram_id,
    full_name,
    national_id,
    phone_number,
    mobile_money,
    employment_status
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT OR REPLACE INTO users
        (
        telegram_id,
        full_name,
        national_id,
        phone_number,
        mobile_money,
        employment_status
        )

        VALUES(?,?,?,?,?,?)
        """,
        (
            telegram_id,
            full_name,
            national_id,
            phone_number,
            mobile_money,
            employment_status
        )
    )


    conn.commit()

    conn.close()
    # ================= SAVE LOAN =================

def save_loan(
    telegram_id,
    purpose,
    amount
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO loans
        (
        telegram_id,
        purpose,
        amount
        )

        VALUES(?,?,?)
        """,
        (
            telegram_id,
            purpose,
            amount
        )
    )


    conn.commit()

    conn.close()





# ================= INTEREST CALCULATION =================

def calculate_interest(amount):

    if amount <= 20000:

        rate = 3

    elif amount <= 100000:

        rate = 5

    elif amount <= 500000:

        rate = 7

    else:

        rate = 9



    interest = amount * rate / 100


    return rate, interest





# ================= REPAYMENT CALCULATION =================

def create_repayment_schedule(
    loan_id,
    period
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()



    cursor.execute(
        """
        SELECT amount
        FROM loans
        WHERE id=?
        """,
        (loan_id,)
    )


    loan = cursor.fetchone()


    if not loan:

        conn.close()

        return



    amount = loan[0]



    rate, interest = calculate_interest(
        amount
    )


    total = amount + interest


    monthly = total / period


    next_date = (
        datetime.now()
        +
        timedelta(
            days=30
        )
    ).strftime(
        "%Y-%m-%d"
    )



    cursor.execute(
        """
        UPDATE loans

        SET interest_rate=?,

        interest_amount=?,

        total_repayment=?,

        repayment_period=?,

        monthly_payment=?,

        remaining_balance=?,

        next_payment_date=?,

        payment_status='Pending'

        WHERE id=?

        """,
        (
            rate,
            interest,
            total,
            period,
            monthly,
            total,
            next_date,
            loan_id
        )
    )



    conn.commit()

    conn.close()





# ================= GET LOANS =================

def get_loans(
    telegram_id
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *
        FROM loans
        WHERE telegram_id=?
        """,
        (
            telegram_id,
        )
    )


    data = cursor.fetchall()


    conn.close()


    return data





# ================= GET ALL LOANS =================

def get_all_loans():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute(
        "SELECT * FROM loans"
    )


    data = cursor.fetchall()


    conn.close()


    return data





# ================= GET USER =================

def get_user_by_id(
    telegram_id
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE telegram_id=?
        """,
        (
            telegram_id,
        )
    )


    user = cursor.fetchone()


    conn.close()


    return user
    # ================= GET USERS =================

def get_users():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute(
        "SELECT * FROM users"
    )


    users = cursor.fetchall()


    conn.close()


    return users





# ================= SEARCH USER =================

def search_user(value):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE phone_number=?
        OR national_id=?
        """,
        (
            value,
            value
        )
    )


    user = cursor.fetchone()


    conn.close()


    return user





# ================= UPDATE LOAN STATUS =================

def update_loan_status(
    loan_id,
    status
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE loans
        SET status=?
        WHERE id=?
        """,
        (
            status,
            loan_id
        )
    )


    conn.commit()

    conn.close()





# ================= SAVE LOAN DECISION =================

def save_loan_decision(
    loan_id,
    note,
    date
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE loans

        SET decision_note=?,
            decision_date=?

        WHERE id=?

        """,
        (
            note,
            date,
            loan_id
        )
    )


    conn.commit()

    conn.close()





# ================= OTP SYSTEM =================

def generate_otp():

    return str(
        random.randint(
            100000,
            999999
        )
    )




def save_otp(
    telegram_id,
    otp
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO otp
        (
        telegram_id,
        otp,
        created_at
        )

        VALUES(?,?,?)
        """,
        (
            telegram_id,
            otp,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
    )


    conn.commit()

    conn.close()





def verify_otp(
    telegram_id,
    otp
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *
        FROM otp
        WHERE telegram_id=?
        AND otp=?
        """,
        (
            telegram_id,
            otp
        )
    )


    result = cursor.fetchone()


    if result:

        cursor.execute(
            """
            UPDATE users
            SET verified='Yes'
            WHERE telegram_id=?
            """,
            (
                telegram_id,
            )
        )


    conn.commit()

    conn.close()


    return result is not None





# ================= PROFILE =================

def get_profile(
    telegram_id
):

    return get_user_by_id(
        telegram_id
    )





def update_profile(
    telegram_id,
    phone,
    mobile,
    employment
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE users

        SET phone_number=?,
            mobile_money=?,
            employment_status=?

        WHERE telegram_id=?

        """,
        (
            phone,
            mobile,
            employment,
            telegram_id
        )
    )


    conn.commit()

    conn.close()





# ================= PAYMENT SYSTEM =================

def record_payment(
    telegram_id,
    loan_id,
    amount
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()



    cursor.execute(
        """
        INSERT INTO payments

        (
        telegram_id,
        loan_id,
        amount,
        payment_date
        )

        VALUES(?,?,?,?)

        """,
        (
            telegram_id,
            loan_id,
            amount,
            datetime.now().strftime(
                "%Y-%m-%d"
            )
        )
    )



    cursor.execute(
        """
        UPDATE loans

        SET remaining_balance =
        remaining_balance - ?

        WHERE id=?

        """,
        (
            amount,
            loan_id
        )
    )


    conn.commit()

    conn.close()





# ================= ADMIN LOG =================

def log_admin_action(
    admin_id,
    action,
    loan_id
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO admin_logs

        (
        admin_id,
        action,
        loan_id,
        created_at
        )

        VALUES(?,?,?,?)

        """,
        (
            admin_id,
            action,
            loan_id,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
    )


    conn.commit()

    conn.close()





# ================= STATISTICS =================

def get_loan_statistics():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()



    cursor.execute(
        "SELECT COUNT(*) FROM loans"
    )

    total = cursor.fetchone()[0]



    cursor.execute(
        """
        SELECT COUNT(*)
        FROM loans
        WHERE status='Pending'
        """
    )

    pending = cursor.fetchone()[0]



    cursor.execute(
        """
        SELECT COUNT(*)
        FROM loans
        WHERE status='Approved'
        """
    )

    approved = cursor.fetchone()[0]



    cursor.execute(
        """
        SELECT COUNT(*)
        FROM loans
        WHERE status='Rejected'
        """
    )

    rejected = cursor.fetchone()[0]



    cursor.execute(
        "SELECT SUM(amount) FROM loans"
    )

    amount = cursor.fetchone()[0]



    conn.close()


    return (
        total,
        pending,
        approved,
        rejected,
        amount or 0
    )





# ================= DATABASE UPDATE COMPATIBILITY =================

def update_database_structure():

    create_database()
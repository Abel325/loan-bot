import sqlite3

conn = sqlite3.connect("loan_bot.db")
cursor = conn.cursor()

cursor.execute("""
SELECT
    id,
    telegram_id,
    full_name,
    national_id,
    phone_number,
    mobile_money,
    employment_status
FROM users
""")

users = cursor.fetchall()

print("\n===== REGISTERED CLIENTS =====\n")

for user in users:
    print(f"ID: {user[0]}")
    print(f"Telegram ID: {user[1]}")
    print(f"Full Name: {user[2]}")
    print(f"National ID: {user[3]}")
    print(f"Phone: {user[4]}")
    print(f"Mobile Money: {user[5]}")
    print(f"Employment: {user[6]}")
    print("-" * 40)

conn.close()
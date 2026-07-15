from telegram import ReplyKeyboardMarkup, KeyboardButton


# Start/Register button
def register_keyboard():
    keyboard = [
        ["📝 Register"]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


# Main menu after registration
def main_menu_keyboard():
    keyboard = [
        ["💰 Apply for Loan"],
        ["📋 Check Loan Status"],
        ["ℹ️ Loan Requirements"],
        ["📞 Contact Support"]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


# Employment status options
def employment_keyboard():
    keyboard = [
        ["Employed"],
        ["Self Employed"],
        ["Business Owner"],
        ["Unemployed"]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )


# Loan amount buttons
def loan_amount_keyboard():
    keyboard = [
        ["KSh 5,000", "KSh 10,000"],
        ["KSh 15,000", "KSh 20,000"],
        ["KSh 25,000", "KSh 30,000"],
        ["KSh 50,000", "KSh 100,000"],
        ["KSh 200,000", "KSh 500,000"],
        ["KSh 1,000,000"]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )


# Cancel button
def cancel_keyboard():
    keyboard = [
        ["❌ Cancel"]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

from telegram import (
    ReplyKeyboardMarkup
)


# ================= REGISTER =================

def register_keyboard():

    keyboard = [
        
    

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


# ================= EMPLOYMENT =================

def employment_keyboard():

    keyboard = [

        ["Employed"],

        ["Self Employed"],

        ["Business Owner"],

        ["Student"],

        ["Unemployed"]

    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )


# ================= LOAN AMOUNT =================

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
        resize_keyboard=True
    )


# ================= REPAYMENT PERIOD =================

def repayment_period_keyboard():

    keyboard = [

        ["1 Month", "3 Months"],

        ["6 Months", "12 Months"],

        ["18 Months", "24 Months"]

    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )


# ================= MAIN MENU =================

def main_menu_keyboard():

    keyboard = [

        ["💰 Apply for Loan"],

        ["📋 Check Loan Status", "📄 Loan Statement"],

        ["💳 Make Payment", "📅 Repayment Schedule"],

        ["👤 My Profile", "✏️ Update Profile"],

        ["ℹ️ Loan Requirements", "📞 Contact Support"]

    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


# ================= ADMIN MENU =================

def admin_keyboard():

    keyboard = [

        ["📊 Dashboard"],

        ["👥 Users", "📋 Loans"],

        ["💳 Payments", "🚚 Disbursements"],

        ["📤 Export Reports"]

    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

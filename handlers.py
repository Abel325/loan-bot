from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters
)

from database import save_user, save_loan, get_user, get_loans
from keyboards import (
    register_keyboard,
    main_menu_keyboard,
    employment_keyboard,
    loan_amount_keyboard
)

from states import (
    FULL_NAME,
    NATIONAL_ID,
    PHONE_NUMBER,
    MOBILE_MONEY,
    EMPLOYMENT_STATUS,
    LOAN_PURPOSE,
    LOAN_AMOUNT
)

from config import SUPPORT_CONTACT


# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👋 Welcome to Official Waafi Loan Assistant!\n\n"
        "We provide a simple loan application service.\n"
        "Please register to continue.",
        reply_markup=register_keyboard()
    )


# ================= REGISTRATION =================

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Please enter your Full Name:"
    )

    return FULL_NAME


async def full_name(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["full_name"] = update.message.text

    await update.message.reply_text(
        "Enter your National ID number:"
    )

    return NATIONAL_ID


async def national_id(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["national_id"] = update.message.text

    await update.message.reply_text(
        "Enter your phone number:"
    )

    return PHONE_NUMBER


async def phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["phone_number"] = update.message.text

    await update.message.reply_text(
        "Enter your Mobile Money number:"
    )

    return MOBILE_MONEY


async def mobile_money(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["mobile_money"] = update.message.text

    await update.message.reply_text(
        "Select your employment status:",
        reply_markup=employment_keyboard()
    )

    return EMPLOYMENT_STATUS


async def employment_status(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["employment_status"] = update.message.text

    save_user(
        update.effective_user.id,
        context.user_data["full_name"],
        context.user_data["national_id"],
        context.user_data["phone_number"],
        context.user_data["mobile_money"],
        context.user_data["employment_status"]
    )

    await update.message.reply_text(
        "✅ Registration complete!",
        reply_markup=main_menu_keyboard()
    )

    return ConversationHandler.END


# ================= LOAN APPLICATION =================

async def apply_loan(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "What is the purpose of your loan?"
    )

    return LOAN_PURPOSE


async def loan_purpose(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["loan_purpose"] = update.message.text

    await update.message.reply_text(
        "Select loan amount:",
        reply_markup=loan_amount_keyboard()
    )

    return LOAN_AMOUNT


async def loan_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):

    amount = update.message.text

    amount = amount.replace("KSh ", "")
    amount = amount.replace(",", "")

    save_loan(
        update.effective_user.id,
        context.user_data["loan_purpose"],
        int(amount)
    )

    await update.message.reply_text(
        "✅ Loan application submitted successfully.\n"
        "Status: Pending",
        reply_markup=main_menu_keyboard()
    )

    return ConversationHandler.END


# ================= LOAN STATUS =================

async def loan_status(update: Update, context: ContextTypes.DEFAULT_TYPE):

    loans = get_loans(update.effective_user.id)

    if not loans:
        await update.message.reply_text(
            "You have no loan applications."
        )
        return

    message = "📋 Your Loan Applications:\n\n"

    for loan in loans:
        message += (
            f"Amount: KSh {loan[3]:,}\n"
            f"Purpose: {loan[2]}\n"
            f"Status: {loan[4]}\n\n"
        )

    await update.message.reply_text(message)


# ================= INFORMATION =================

async def requirements(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "ℹ️ Loan Requirements:\n\n"
        "✅ Valid National ID\n"
        "✅ Active Phone Number\n"
        "✅ Mobile Money Account\n"
        "✅ Employment or Business Information"
    )


async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        f"📞 Contact Support:\n{SUPPORT_CONTACT}"
    )

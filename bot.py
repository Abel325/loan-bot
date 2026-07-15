from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters
)

from config import BOT_TOKEN
from database import create_tables

from handlers import (
    start,
    register,
    full_name,
    national_id,
    phone_number,
    mobile_money,
    employment_status,
    apply_loan,
    loan_purpose,
    loan_amount,
    loan_status,
    requirements,
    support
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


def main():

    # Create database tables
    create_tables()

    app = Application.builder().token(BOT_TOKEN).build()


    # Registration conversation
    registration_handler = ConversationHandler(
        entry_points=[
            MessageHandler(
                filters.Regex("^📝 Register$"),
                register
            )
        ],

        states={

            FULL_NAME: [
                MessageHandler(
                    filters.TEXT,
                    full_name
                )
            ],

            NATIONAL_ID: [
                MessageHandler(
                    filters.TEXT,
                    national_id
                )
            ],

            PHONE_NUMBER: [
                MessageHandler(
                    filters.TEXT,
                    phone_number
                )
            ],

            MOBILE_MONEY: [
                MessageHandler(
                    filters.TEXT,
                    mobile_money
                )
            ],

            EMPLOYMENT_STATUS: [
                MessageHandler(
                    filters.TEXT,
                    employment_status
                )
            ]
        },

        fallbacks=[]
    )


    # Loan application conversation
    loan_handler = ConversationHandler(
        entry_points=[
            MessageHandler(
                filters.Regex("^💰 Apply for Loan$"),
                apply_loan
            )
        ],

        states={

            LOAN_PURPOSE: [
                MessageHandler(
                    filters.TEXT,
                    loan_purpose
                )
            ],

            LOAN_AMOUNT: [
                MessageHandler(
                    filters.TEXT,
                    loan_amount
                )
            ]
        },

        fallbacks=[]
    )


    # Commands
    app.add_handler(
        CommandHandler("start", start)
    )


    # Conversations
    app.add_handler(registration_handler)
    app.add_handler(loan_handler)


    # Menu buttons
    app.add_handler(
        MessageHandler(
            filters.Regex("^📋 Check Loan Status$"),
            loan_status
        )
    )

    app.add_handler(
        MessageHandler(
            filters.Regex("^ℹ️ Loan Requirements$"),
            requirements
        )
    )

    app.add_handler(
        MessageHandler(
            filters.Regex("^📞 Contact Support$"),
            support
        )
    )


    print("🤖 Waafi Loan Bot is running...")

    app.run_polling()



if __name__ == "__main__":
    main()

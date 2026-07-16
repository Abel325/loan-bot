from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters
)


from database import (
    create_database,
    update_database_structure
)


from handlers import (

    start,

    register,
    full_name,
    national_id,
    phone_number,
    mobile_money,
    employment_status,
    verify_user_otp,

    apply_loan,
    loan_purpose,
    loan_amount,

    loan_status,
    my_profile,
    update_profile_start,
    update_phone,
    update_mobile_money,
    update_employment,
    loan_statement,

    requirements,
    support,

    admin_panel,
    admin_buttons,

    approve_loan,
    reject_loan,
    save_approval_note,
    save_rejection_reason

)


from states import (

    FULL_NAME,
    NATIONAL_ID,
    PHONE_NUMBER,
    MOBILE_MONEY,
    EMPLOYMENT_STATUS,

    LOAN_PURPOSE,
    LOAN_AMOUNT,

    OTP_INPUT,

    UPDATE_PHONE,
    UPDATE_MOBILE_MONEY,
    UPDATE_EMPLOYMENT,

    APPROVAL_NOTE,
    REJECTION_REASON

)


from config import TOKEN



def main():


    create_database()


    update_database_structure()



    app = Application.builder().token(TOKEN).build()



    # ================= START =================

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )



    # ================= USER CONVERSATION =================

    user_conversation = ConversationHandler(

        entry_points=[


            MessageHandler(
                filters.Regex("^📝 Register$"),
                register
            ),


            MessageHandler(
                filters.Regex("^💰 Apply for Loan$"),
                apply_loan
            ),


            MessageHandler(
                filters.Regex("^✏️ Update Profile$"),
                update_profile_start
            )


        ],


        states={


            FULL_NAME:[

                MessageHandler(
                    filters.TEXT,
                    full_name
                )

            ],


            NATIONAL_ID:[

                MessageHandler(
                    filters.TEXT,
                    national_id
                )

            ],


            PHONE_NUMBER:[

                MessageHandler(
                    filters.TEXT,
                    phone_number
                )

            ],


            MOBILE_MONEY:[

                MessageHandler(
                    filters.TEXT,
                    mobile_money
                )

            ],


            EMPLOYMENT_STATUS:[

                MessageHandler(
                    filters.TEXT,
                    employment_status
                )

            ],


            OTP_INPUT:[

                MessageHandler(
                    filters.TEXT,
                    verify_user_otp
                )

            ],


            LOAN_PURPOSE:[

                MessageHandler(
                    filters.TEXT,
                    loan_purpose
                )

            ],


            LOAN_AMOUNT:[

                MessageHandler(
                    filters.TEXT,
                    loan_amount
                )

            ],


            UPDATE_PHONE:[

                MessageHandler(
                    filters.TEXT,
                    update_phone
                )

            ],


            UPDATE_MOBILE_MONEY:[

                MessageHandler(
                    filters.TEXT,
                    update_mobile_money
                )

            ],


            UPDATE_EMPLOYMENT:[

                MessageHandler(
                    filters.TEXT,
                    update_employment
                )

            ],
                        APPROVAL_NOTE:[

                MessageHandler(
                    filters.TEXT,
                    save_approval_note
                )

            ],


            REJECTION_REASON:[

                MessageHandler(
                    filters.TEXT,
                    save_rejection_reason
                )

            ]

        },


        fallbacks=[]

    )



    app.add_handler(
        user_conversation
    )



    # ================= USER MENU =================


    app.add_handler(

        MessageHandler(
            filters.Regex("^📋 Check Loan Status$"),
            loan_status
        )

    )



    app.add_handler(

        MessageHandler(
            filters.Regex("^👤 My Profile$"),
            my_profile
        )

    )



    app.add_handler(

        MessageHandler(
            filters.Regex("^📄 Loan Statement$"),
            loan_statement
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



    # ================= ADMIN =================


    app.add_handler(

        CommandHandler(
            "admin",
            admin_panel
        )

    )



    app.add_handler(

        CallbackQueryHandler(
            admin_buttons,
            pattern="^(users|loans|stats)$"
        )

    )



    app.add_handler(

        CallbackQueryHandler(
            approve_loan,
            pattern="^approve_"
        )

    )



    app.add_handler(

        CallbackQueryHandler(
            reject_loan,
            pattern="^reject_"
        )

    )



    print(
        "🤖 Waafi Loan Bot Version 2 Running..."
    )



    app.run_polling(
        drop_pending_updates=True
    )




if __name__ == "__main__":

    main()
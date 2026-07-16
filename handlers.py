from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ContextTypes,
    ConversationHandler
)

from database import (
    save_user,
    save_loan,
    get_loans,
    get_users,
    get_all_loans,
    get_user_by_id,
    get_loan_statistics,
    search_user,
    update_loan_status,
    save_loan_decision,

    generate_otp,
    save_otp,
    verify_otp,
    get_profile,
    update_profile
)

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
    LOAN_AMOUNT,

    APPROVAL_NOTE,
    REJECTION_REASON,

    OTP_INPUT,
    UPDATE_PHONE,
    UPDATE_MOBILE_MONEY,
    UPDATE_EMPLOYMENT,
    STATEMENT_REQUEST
)

from config import (
    SUPPORT_CONTACT,
    ADMIN_ID
)

from datetime import datetime



# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👋 Welcome to Official Waafi Loan Assistant!\n\n"
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
        "Enter your National ID:"
    )

    return NATIONAL_ID



async def national_id(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["national_id"] = update.message.text


    await update.message.reply_text(
        "Enter your Phone Number:"
    )

    return PHONE_NUMBER



async def phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["phone_number"] = update.message.text


    await update.message.reply_text(
        "Enter your Mobile Money Number:"
    )

    return MOBILE_MONEY



async def mobile_money(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["mobile_money"] = update.message.text


    await update.message.reply_text(
        "Select Employment Status:",
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


    otp = generate_otp()


    save_otp(
        update.effective_user.id,
        otp
    )


    await update.message.reply_text(

        "✅ Registration completed!\n\n"
        "🔐 OTP Verification\n\n"
        f"Your OTP code is: {otp}\n\n"
        "Enter the code to verify your account."

    )


    return OTP_INPUT



# ================= VERIFY OTP =================

async def verify_user_otp(update: Update, context: ContextTypes.DEFAULT_TYPE):

    otp = update.message.text


    if verify_otp(
        update.effective_user.id,
        otp
    ):


        await update.message.reply_text(

            "✅ Account verified successfully!",

            reply_markup=main_menu_keyboard()

        )


    else:

        await update.message.reply_text(
            "❌ Wrong OTP. Try again."
        )

        return OTP_INPUT


    return ConversationHandler.END



# ================= LOAN APPLICATION =================

async def apply_loan(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "What is the purpose of the loan?"
    )


    return LOAN_PURPOSE



async def loan_purpose(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["loan_purpose"] = update.message.text


    await update.message.reply_text(

        "🎉 Congratulations!\n\n"
        "You pre-qualify for up to KSh 1,000,000.\n\n"
        "Select loan amount:",

        reply_markup=loan_amount_keyboard()

    )


    return LOAN_AMOUNT



async def loan_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):

    amount = update.message.text.replace(
        "KSh ",
        ""
    ).replace(
        ",",
        ""
    )


    save_loan(

        update.effective_user.id,

        context.user_data["loan_purpose"],

        int(amount)

    )


    await update.message.reply_text(

        "✅ Loan application submitted successfully.\n\n"
        "Status: Pending",

        reply_markup=main_menu_keyboard()

    )


    return ConversationHandler.END
    # ================= LOAN STATUS =================

async def loan_status(update: Update, context: ContextTypes.DEFAULT_TYPE):

    loans = get_loans(
        update.effective_user.id
    )


    if not loans:

        await update.message.reply_text(
            "You have no loan applications."
        )

        return


    text = "📋 YOUR LOAN APPLICATIONS\n\n"


    for loan in loans:

        text += (

            f"🆔 Loan ID: {loan[0]}\n"
            f"💰 Amount: KSh {loan[3]:,}\n"
            f"📝 Purpose: {loan[2]}\n"
            f"📌 Status: {loan[4]}\n"

        )


        if len(loan) > 5 and loan[5]:

            text += (
                f"📄 Decision: {loan[5]}\n"
            )


        if len(loan) > 6 and loan[6]:

            text += (
                f"📅 Date: {loan[6]}\n"
            )


        text += "\n"


    await update.message.reply_text(text)



# ================= MY PROFILE =================

async def my_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = get_profile(
        update.effective_user.id
    )


    if not user:

        await update.message.reply_text(
            "❌ Profile not found."
        )

        return



    verified = "No"


    if len(user) > 7 and user[7]:

        verified = user[7]



    await update.message.reply_text(

        "👤 MY PROFILE\n\n"

        f"Name: {user[2]}\n"
        f"National ID: {user[3]}\n"
        f"Phone: {user[4]}\n"
        f"Mobile Money: {user[5]}\n"
        f"Employment: {user[6]}\n"
        f"Verified: {verified}"

    )



# ================= UPDATE PROFILE START =================

async def update_profile_start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(

        "Enter new phone number:"

    )


    return UPDATE_PHONE



async def update_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["new_phone"] = update.message.text


    await update.message.reply_text(

        "Enter new mobile money number:"

    )


    return UPDATE_MOBILE_MONEY



async def update_mobile_money(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["new_mobile"] = update.message.text


    await update.message.reply_text(

        "Select employment status:",

        reply_markup=employment_keyboard()

    )


    return UPDATE_EMPLOYMENT



async def update_employment(update: Update, context: ContextTypes.DEFAULT_TYPE):

    update_profile(

        update.effective_user.id,

        context.user_data["new_phone"],

        context.user_data["new_mobile"],

        update.message.text

    )


    await update.message.reply_text(

        "✅ Profile updated successfully.",

        reply_markup=main_menu_keyboard()

    )


    return ConversationHandler.END



# ================= LOAN STATEMENT =================

async def loan_statement(update: Update, context: ContextTypes.DEFAULT_TYPE):

    loans = get_loans(

        update.effective_user.id

    )


    if not loans:

        await update.message.reply_text(

            "❌ No loan statement available."

        )

        return



    statement = "📄 WAAFI LOAN STATEMENT\n\n"



    for loan in loans:

        statement += (

            f"Statement ID: {loan[6] if len(loan)>6 else 'N/A'}\n"

            f"Loan ID: {loan[0]}\n"

            f"Amount: KSh {loan[3]:,}\n"

            f"Purpose: {loan[2]}\n"

            f"Status: {loan[4]}\n"

        )


        if len(loan) > 5 and loan[5]:

            statement += (

                f"Decision: {loan[5]}\n"

            )


        if len(loan) > 7 and loan[7]:

            statement += (

                f"Decision Date: {loan[7]}\n"

            )


        statement += "\n"



    await update.message.reply_text(statement)



# ================= REQUIREMENTS =================

async def requirements(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(

        "ℹ️ LOAN REQUIREMENTS\n\n"
        "✅ Valid National ID\n"
        "✅ Active Phone Number\n"
        "✅ Mobile Money Account\n"
        "✅ Employment Information"

    )



# ================= SUPPORT =================

async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(

        f"📞 Support\n\n{SUPPORT_CONTACT}"

    )
    # ================= ADMIN PANEL =================

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:

        await update.message.reply_text(
            "❌ You are not authorized."
        )

        return


    keyboard = [

        [
            InlineKeyboardButton(
                "👥 View Users",
                callback_data="users"
            )
        ],

        [
            InlineKeyboardButton(
                "📋 View Loans",
                callback_data="loans"
            )
        ],

        [
            InlineKeyboardButton(
                "📊 Statistics",
                callback_data="stats"
            )
        ]

    ]


    await update.message.reply_text(

        "👨‍💼 WAAFI ADMIN PANEL",

        reply_markup=InlineKeyboardMarkup(keyboard)

    )



# ================= ADMIN BUTTONS =================

async def admin_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()



    if query.data == "users":

        users = get_users()


        text = "👥 REGISTERED USERS\n\n"


        for user in users:

            text += (

                f"👤 {user[2]}\n"
                f"🆔 {user[3]}\n"
                f"📞 {user[4]}\n"
                f"💼 {user[6]}\n\n"

            )


        await query.edit_message_text(text)



    elif query.data == "loans":

        loans = get_all_loans()


        for loan in loans:

            user = get_user_by_id(
                loan[1]
            )


            details = ""


            if user:

                details = (

                    f"👤 Name: {user[2]}\n"
                    f"🆔 ID: {user[3]}\n"
                    f"📞 Phone: {user[4]}\n"
                    f"💼 Job: {user[6]}\n\n"

                )



            keyboard = [

                [

                    InlineKeyboardButton(
                        "✅ Approve",
                        callback_data=f"approve_{loan[0]}"
                    ),

                    InlineKeyboardButton(
                        "❌ Reject",
                        callback_data=f"reject_{loan[0]}"
                    )

                ]

            ]



            await query.message.reply_text(

                "📋 LOAN APPLICATION\n\n"

                f"{details}"

                f"💰 Amount: KSh {loan[3]:,}\n"
                f"📝 Purpose: {loan[2]}\n"
                f"📌 Status: {loan[4]}",

                reply_markup=InlineKeyboardMarkup(keyboard)

            )



    elif query.data == "stats":


        total, pending, approved, rejected, amount = get_loan_statistics()


        await query.edit_message_text(

            "📊 WAAFI STATISTICS\n\n"

            f"💰 Total Loans: {total}\n"
            f"⏳ Pending: {pending}\n"
            f"✅ Approved: {approved}\n"
            f"❌ Rejected: {rejected}\n"
            f"💵 Amount: KSh {amount:,}"

        )



# ================= APPROVE LOAN =================

async def approve_loan(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()


    loan_id = query.data.split("_")[1]


    context.user_data["loan_id"] = loan_id


    await query.message.reply_text(

        "📝 Enter approval note:"

    )


    return APPROVAL_NOTE



async def save_approval_note(update: Update, context: ContextTypes.DEFAULT_TYPE):

    note = update.message.text

    loan_id = context.user_data["loan_id"]


    update_loan_status(

        loan_id,

        "Approved"

    )


    save_loan_decision(

        loan_id,

        note,

        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    )



    loans = get_all_loans()


    for loan in loans:

        if str(loan[0]) == str(loan_id):

            await context.bot.send_message(

                chat_id=loan[1],

                text=(

                    "🎉 LOAN APPROVED\n\n"

                    "Your loan has been approved.\n\n"

                    f"📝 Note:\n{note}"

                )

            )


            break



    await update.message.reply_text(

        "✅ Approved and applicant notified."

    )


    return ConversationHandler.END



# ================= REJECT LOAN =================

async def reject_loan(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()


    loan_id = query.data.split("_")[1]


    context.user_data["loan_id"] = loan_id


    await query.message.reply_text(

        "📝 Enter rejection reason:"

    )


    return REJECTION_REASON



async def save_rejection_reason(update: Update, context: ContextTypes.DEFAULT_TYPE):

    reason = update.message.text

    loan_id = context.user_data["loan_id"]



    update_loan_status(

        loan_id,

        "Rejected"

    )



    save_loan_decision(

        loan_id,

        reason,

        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    )



    loans = get_all_loans()


    for loan in loans:

        if str(loan[0]) == str(loan_id):


            await context.bot.send_message(

                chat_id=loan[1],

                text=(

                    "❌ LOAN REJECTED\n\n"

                    "Your loan application has been rejected.\n\n"

                    f"Reason:\n{reason}"

                )

            )


            break



    await update.message.reply_text(

        "❌ Rejected and applicant notified."

    )


    return ConversationHandler.END
    
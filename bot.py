from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8870513554:AAEeAGTRpr9E9PvtW-znaRfhQJZmZser0Bo"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Official Waafi Loan Assistant!"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("🤖 Waafi Loan Bot is running...")

    app.run_polling()

if __name__ == "__main__":
    main()
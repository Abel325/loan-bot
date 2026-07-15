import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = os.getenv("ADMIN_ID")

DATABASE_NAME = "loanbot.db"

SUPPORT_CONTACT = "@YourSupportUsername"

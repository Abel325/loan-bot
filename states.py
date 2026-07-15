from telegram.ext import ConversationHandler


# Registration states
FULL_NAME = 1
NATIONAL_ID = 2
PHONE_NUMBER = 3
MOBILE_MONEY = 4
PIN=4
EMPLOYMENT_STATUS = 5


# Loan application states
LOAN_PURPOSE = 6
LOAN_AMOUNT = 7


# Export all states
REGISTRATION_STATES = (
    FULL_NAME,
    NATIONAL_ID,
    PHONE_NUMBER,
    MOBILE_MONEY,
    EMPLOYMENT_STATUS
)

LOAN_STATES = (
    LOAN_PURPOSE,
    LOAN_AMOUNT
)

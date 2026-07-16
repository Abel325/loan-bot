# ================= REGISTRATION =================

(
    FULL_NAME,
    NATIONAL_ID,
    PHONE_NUMBER,
    MOBILE_MONEY,
    EMPLOYMENT_STATUS,
) = range(5)


# ================= OTP =================

OTP_INPUT = 5


# ================= LOAN APPLICATION =================

(
    LOAN_PURPOSE,
    LOAN_AMOUNT,
    REPAYMENT_PERIOD,
) = range(6, 9)


# ================= PROFILE =================

(
    UPDATE_PHONE,
    UPDATE_MOBILE_MONEY,
    UPDATE_EMPLOYMENT,
) = range(9, 12)


# ================= PAYMENTS =================

(
    MAKE_PAYMENT,
    PAYMENT_AMOUNT,
) = range(12, 14)


# ================= ADMIN =================

(
    APPROVAL_NOTE,
    REJECTION_REASON,
    DISBURSEMENT_STATUS,
) = range(14, 17)


# ================= REPORTS =================

EXPORT_REPORT = 17


# ================= STATEMENTS =================

STATEMENT_REQUEST = 18
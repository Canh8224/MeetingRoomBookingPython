from sqlalchemy import Column, String, DateTime

from database import Base


class PasswordResetOtp(Base):
    __tablename__ = "password_reset_otps"

    otp = Column(
        String(255),
        primary_key=True
    )

    email = Column(
        String(255)
    )

    expiry_date = Column(
        "expiryDate",
        DateTime
    )

    created_date = Column(
        "createdDate",
        DateTime
    )
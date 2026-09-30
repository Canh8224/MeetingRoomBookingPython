from sqlalchemy import Column, String, DateTime

from database import Base


class InvalidatedToken(Base):
    __tablename__ = "invalidated_token"

    id = Column(
        String(255),
        primary_key=True
    )

    expiry_time = Column(
        "expiryTime",
        DateTime,
        nullable=False
    )
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Notification(Base):
    __tablename__ = "notifications"

    notification_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    content = Column(
        String(255)
    )

    type = Column(
        String(20),
        nullable=False
    )

    has_read = Column(
        "hasRead",
        Boolean,
        nullable=False
    )

    user_id = Column(
        "user_id",
        BigInteger,
        ForeignKey("users.user_id"),
        nullable=True
    )

    created_at = Column(
        "created_at",
        DateTime
    )

    user = relationship(
        "User",
        back_populates="notifications"
    )
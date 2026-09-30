from sqlalchemy import Column, String, Text

from database import Base


class Permission(Base):
    __tablename__ = "permissions"

    permission_name = Column(
        String(50),
        primary_key=True,
        nullable=False,
        unique=True
    )

    description = Column(
        Text
    )
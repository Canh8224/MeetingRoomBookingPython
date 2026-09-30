from sqlalchemy import Column, String, Text

from database import Base


class Position(Base):
    __tablename__ = "positions"

    position_name = Column(
        String(75),
        primary_key=True,
        nullable=False,
        unique=True
    )

    description = Column(
        Text
    )
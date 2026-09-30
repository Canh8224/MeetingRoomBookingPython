from sqlalchemy import Column, String, DateTime

from database import Base


class GroupEntity(Base):
    __tablename__ = "groups"

    group_name = Column(
        String(50),
        primary_key=True,
        nullable=False
    )

    location = Column(
        String(100)
    )

    division = Column(
        String(50)
    )

    created_date = Column(
        "createdDate",
        DateTime
    )
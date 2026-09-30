from sqlalchemy import Column, BigInteger, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from models.associations import user_roles


class User(Base):
    __tablename__ = "users"

    user_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    user_name = Column(
        String(50),
        unique=True,
        nullable=False
    )

    full_name = Column(
        String(100)
    )

    department = Column(
        String(50)
    )

    email = Column(
        String(50),
        unique=True
    )

    phone_number = Column(
        String(20)
    )

    position_id = Column(
        "positionId",
        String(75),
        ForeignKey("positions.position_name", ondelete="SET NULL")
    )

    password = Column(
        String(255),
        nullable=False
    )

    enabled = Column(
        Boolean,
        nullable=False
    )

    group_id = Column(
        "groupId",
        String(50),
        ForeignKey("groups.group_name", ondelete="SET NULL")
    )

    position = relationship(
        "Position"
    )

    group = relationship(
        "GroupEntity"
    )

    notifications = relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    roles = relationship(
        "Role",
        secondary=user_roles
    )
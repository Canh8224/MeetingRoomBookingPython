from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from database import Base
from models.associations import role_permissions


class Role(Base):
    __tablename__ = "roles"

    role_name = Column(
        String(50),
        primary_key=True,
        nullable=False,
        unique=True
    )

    description = Column(
        Text
    )

    permissions = relationship(
        "Permission",
        secondary=role_permissions
    )
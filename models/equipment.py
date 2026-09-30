from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from database import Base


class Equipment(Base):
    __tablename__ = "equipments"

    equipment_name = Column(
        String(50),
        primary_key=True,
        nullable=False
    )

    description = Column(
        Text
    )

    room_equipments = relationship(
        "RoomEquipment",
        back_populates="equipment",
        cascade="all, delete-orphan"
    )
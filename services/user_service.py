import bcrypt
from sqlalchemy.orm import Session

from models.user import User
from schemas.user import UserCreate


def create_user(db: Session, user_data: UserCreate):
    hashed_password = bcrypt.hashpw(
        user_data.password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    user = User(
        user_name=user_data.user_name,
        full_name=user_data.full_name,
        department=user_data.department,
        email=user_data.email,
        phone_number=user_data.phone_number,
        position_id=user_data.position_id,
        group_id=user_data.group_id,
        password=hashed_password,
        enabled=user_data.enabled
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
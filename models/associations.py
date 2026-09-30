from sqlalchemy import Table, Column, BigInteger, String, ForeignKey
from database import Base


user_roles = Table(
    "user_roles",
    Base.metadata,
    Column(
        "user_id",
        BigInteger,
        ForeignKey("users.user_id"),
        primary_key=True
    ),
    Column(
        "role_name",
        String(50),
        ForeignKey("roles.role_name"),
        primary_key=True
    )
)


role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column(
        "role_name",
        String(50),
        ForeignKey("roles.role_name"),
        primary_key=True
    ),
    Column(
        "permission_name",
        String(50),
        ForeignKey("permissions.permission_name"),
        primary_key=True
    )
)
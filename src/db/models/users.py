from sqlalchemy import String, BigInteger, Integer, Column, Boolean
from sqlalchemy.orm import DeclarativeBase


# This made just because of PEP8 naming
# Class should be named with upper first letter
class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: int = Column("id", Integer, primary_key=True)
    user_id: int = Column("user_id", BigInteger, nullable=False)
    username: str = Column("username", String)
    fullname: str = Column("fullname", String, nullable=False)
    timestamp: int = Column("timestamp", BigInteger, nullable=False)
    is_admin: bool = Column("is_admin", Boolean, default=False)

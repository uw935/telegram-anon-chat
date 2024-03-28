import time

from aiogram import Bot
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models.users import User
from config import (
    DB_URL,
    OWNER_CHAT_ID
)


engine = create_engine(DB_URL)
session = sessionmaker(bind=engine, autoflush=False)


logger.info("Connecting to database")
engine.connect()


async def add_user_to_db(
    *,
    user_id: int,
    username: str,
    fullname: str,
    bot: Bot
) -> bool:
    """
    Function to add some user to database

    :return: False if user already exists, True otherwise
    """

    with session() as db:
        user = db.query(User).filter(User.user_id == user_id).first()

        if user is not None:
            return False

        information_message = f"New user just wrote: "\
            f"username: @{username} "\
            f"| fullname: {fullname} "\
            f"| ID: {user_id}"

        logger.info(information_message)

        await bot.send_message(
            chat_id=OWNER_CHAT_ID,
            text=information_message
        )

        user = User(
            user_id=user_id,
            username=username,
            fullname=fullname,
            timestamp=int(time.time()),
        )

        try:
            db.add(user)
            db.commit()
            db.refresh(user)
        except Exception as e:
            db.rollback()
            logger.exception(e)

    return True

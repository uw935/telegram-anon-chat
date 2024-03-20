from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DB_URL


engine = create_engine(f"{DB_URL}?check_same_thread=False")
session = sessionmaker(bind=engine, autoflush=False)


logger.info("Connecting to database")
engine.connect()

from config import DB_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


engine = create_engine(f"{DB_URL}?check_same_thread=False")
session = sessionmaker(bind=engine, autoflush=False)

engine.connect()

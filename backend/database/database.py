from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

user = os.getenv("DB_USER")
host = os.getenv("DB_HOST")
password = os.getenv("DB_PASSWORD")
port = int(os.getenv("DB_PORT"))
database = os.getenv("DB_DATABASE")

DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




def create_db_and_tables():
    Base.metadata.create_all(bind=engine)
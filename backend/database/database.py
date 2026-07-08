from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from dotenv import load_dotenv
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / ".env")


# =========================
# CONFIGURAÇÃO DO BANCO
# =========================

DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:

    user = os.getenv("DB_USER")
    host = os.getenv("DB_HOST")
    password = os.getenv("DB_PASSWORD")
    port = os.getenv("DB_PORT")
    database = os.getenv("DB_DATABASE")


    DATABASE_URL = (
        f"mysql+pymysql://"
        f"{user}:{password}@{host}:{port}/{database}"
    )



# =========================
# ENGINE
# =========================

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True
)



# =========================
# SESSION
# =========================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)



# =========================
# BASE
# =========================

Base = declarative_base()



# =========================
# DEPENDENCY
# =========================

def get_session():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()



# =========================
# CREATE TABLES
# =========================

def create_db_and_tables():

    Base.metadata.create_all(bind=engine)
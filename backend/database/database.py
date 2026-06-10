from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv
import os
load_dotenv()

user = os.getenv("DB_USER")
host = os.getenv("DB_HOST")
password = os.getenv("DB_PASSWORD")
port = os.getenv("DB_PORT")
database = os.getenv("DB_DATABASE")


DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(DATABASE_URL, echo=True)

def get_db():
    return engine

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


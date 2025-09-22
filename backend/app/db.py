from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)  # echo=True si querés ver SQL
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 👇 schema por defecto = public
metadata = MetaData(schema="public")
Base = declarative_base(metadata=metadata)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


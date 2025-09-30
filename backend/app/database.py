from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

DATABASE_URL: str = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
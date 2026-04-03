import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./rpa.db")

ECHO = os.getenv("DB_ECHO", "false").lower() == "true"

class Base(DeclarativeBase):
    pass
 
 
engine = create_engine(
    DATABASE_URL,
    echo=ECHO,
    connect_args={"check_same_thread": False}
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
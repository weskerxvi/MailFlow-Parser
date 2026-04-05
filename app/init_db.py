from app.database import engine, Base
from app.models import Base
from app.database import engine

from fastapi import FastAPI
from contextlib import asynccontextmanager

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Banco inicializado com sucesso.")

if __name__ == "__main__":
    init_db()
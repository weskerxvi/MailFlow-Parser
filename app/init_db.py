from app.database import engine, Base
from app.models import Order

Base.metadata.create_all(bind=engine)
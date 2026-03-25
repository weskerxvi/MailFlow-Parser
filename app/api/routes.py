from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Order
from app.schemas import OrderSchema

router = APIRouter()

@router.get("/orders", response_model=list[OrderSchema])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()
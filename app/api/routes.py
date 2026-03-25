from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.parser import extract_data
from app.email_reader import email_reader
from app.models import Order
from app.schemas import OrderSchema

router = APIRouter()

@router.get("/orders", response_model=list[OrderSchema])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


@router.post("/process")
def process_emails(db: Session = Depends(get_db)):
    emails = email_reader()
    data_list = extract_data(emails)

    for data in data_list:
        if not data:
            continue

        order = Order(
            number=data["number"],
            client=data["client"],
            value=data["value"]
        )

        db.add(order)

    db.commit()

    return {"message": "Emails processed successfully."}
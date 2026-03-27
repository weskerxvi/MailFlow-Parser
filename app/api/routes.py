from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.parser import extract_data
from app.email_reader import email_reader
from app.models import Order
from app.schemas import OrderSchema
from app.services.reports import generate_report

from app.services.normalize_order import normalize_order


router = APIRouter()

@router.get("/orders", response_model=list[OrderSchema])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


@router.post("/process")
def process_emails(db: Session = Depends(get_db)):
    
    emails = email_reader()
    duplicates = 0
    created = 0
    parsed = extract_data(emails)
    
    for item in parsed:
        normalized = normalize_order(item)

        
        existing_order = db.query(Order).filter(
            Order.number == normalized["number"]
        ).first()

        if existing_order:
            print(f"Updated duplicate: {normalized['number']}")
            existing_order.client = normalized["client"]
            existing_order.value = normalized["value"]
            duplicates += 1

            continue

        order = Order(
            number=normalized["number"],
            client=normalized["client"],
            value=normalized["value"]
        )

        db.add(order)
        created += 1

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e

    return {
        "message": "Emails processed successfully.",
        "created": created,
        "duplicates": duplicates
}

@router.get("/reports")
def get_report(db: Session = Depends(get_db)):
    orders = db.query(Order).all()

    return generate_report(orders)
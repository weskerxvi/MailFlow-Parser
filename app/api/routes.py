from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Order, ProcessingRun
from app.schemas import OrderSchema, ProcessingRunSchema
from app.services.order_pipeline import process_orders_from_email
from app.services.reports import generate_report

router = APIRouter()

@router.get("/orders", response_model=list[OrderSchema])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


@router.post("/process")
def process_emails(db: Session = Depends(get_db)):
    return process_orders_from_email(db)

@router.get("/reports")
def get_report(db: Session = Depends(get_db)):
    orders = db.query(Order).all()

    return generate_report(orders)


@router.get("/processing-runs", response_model=list[ProcessingRunSchema])
def get_processing_runs(db: Session = Depends(get_db)):
    return (
        db.query(ProcessingRun)
        .order_by(ProcessingRun.started_at.desc())
        .all()
    )


@router.get("/processing-runs/{run_id}", response_model=ProcessingRunSchema)
def get_processing_run(run_id: int, db: Session = Depends(get_db)):
    run = db.get(ProcessingRun, run_id)

    if not run:
        raise HTTPException(status_code=404, detail="Processing run not found.")

    return run

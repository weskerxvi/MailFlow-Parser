import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.email_reader import email_reader
from app.models import Order, ProcessingRun
from app.parser import extract_data
from app.services.gmail_reader import read_gmail_messages
from app.services.normalize_order import normalize_order

logger = logging.getLogger(__name__)


def process_orders(db: Session, raw_text: str, source: str) -> dict:
    logger.info("Starting order processing from source=%s", source)
    started_at = datetime.now(timezone.utc)
    run = ProcessingRun(status="running", started_at=started_at)
    db.add(run)
    db.commit()
    db.refresh(run)
    run_id = run.id

    total_read = len([line for line in raw_text.splitlines() if line.strip()])
    updated = 0
    created = 0
    failed = 0
    parsed = extract_data(raw_text)
    ignored = total_read - len(parsed)
    processed_orders = {}

    try:
        for item in parsed:
            try:
                normalized = normalize_order(item)
                order_number = int(normalized["number"])
            except (KeyError, TypeError, ValueError):
                failed += 1
                logger.exception("Failed to normalize parsed order: %s", item)
                continue

            existing_order = processed_orders.get(order_number)

            if not existing_order:
                existing_order = db.query(Order).filter(
                    Order.number == order_number
                ).first()

            if existing_order:
                logger.info("Updated existing order: %s", order_number)
                existing_order.client = normalized["client"]
                existing_order.value = normalized["value"]
                updated += 1
                processed_orders[order_number] = existing_order
                continue

            order = Order(
                number=order_number,
                client=normalized["client"],
                value=normalized["value"],
            )

            db.add(order)
            processed_orders[order_number] = order
            created += 1

        run.status = "completed"
        run.total_read = total_read
        run.total_parsed = len(parsed)
        run.created = created
        run.updated = updated
        run.ignored = ignored
        run.failed = failed
        run.finished_at = datetime.now(timezone.utc)
        db.commit()
        logger.info(
            "Completed order processing run_id=%s source=%s created=%s updated=%s ignored=%s failed=%s",
            run.id,
            source,
            created,
            updated,
            ignored,
            failed,
        )
    except Exception:
        db.rollback()
        run = db.get(ProcessingRun, run_id)
        if run:
            run.status = "failed"
            run.total_read = total_read
            run.total_parsed = len(parsed)
            run.created = created
            run.updated = updated
            run.ignored = ignored
            run.failed = failed
            run.error_message = "Processing transaction failed."
            run.finished_at = datetime.now(timezone.utc)
            db.commit()
        logger.exception("Order processing transaction failed for source=%s", source)
        raise

    db.refresh(run)

    return {
        "run_id": run.id,
        "status": run.status,
        "message": "Emails processed successfully.",
        "source": source,
        "total_read": run.total_read,
        "total_parsed": run.total_parsed,
        "created": created,
        "updated": updated,
        "duplicates": updated,
        "ignored": ignored,
        "failed": failed,
        "started_at": run.started_at,
        "finished_at": run.finished_at,
    }


def process_orders_from_email(db: Session) -> dict:
    emails = email_reader()
    return process_orders(db=db, raw_text=emails, source="local")


def process_orders_from_gmail(db: Session) -> dict:
    emails = read_gmail_messages()
    return process_orders(db=db, raw_text=emails, source="gmail")

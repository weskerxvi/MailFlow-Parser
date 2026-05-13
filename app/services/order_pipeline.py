import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.email_reader import email_reader
from app.models import Order, ProcessingRun
from app.parser import extract_data
from app.services.normalize_order import normalize_order

logger = logging.getLogger(__name__)


def process_orders_from_email(db: Session) -> dict:
    started_at = datetime.now(timezone.utc)
    run = ProcessingRun(status="running", started_at=started_at)
    db.add(run)
    db.commit()
    db.refresh(run)
    run_id = run.id

    emails = email_reader()
    total_read = len([line for line in emails.splitlines() if line.strip()])
    updated = 0
    created = 0
    failed = 0
    parsed = extract_data(emails)
    ignored = total_read - len(parsed)

    try:
        for item in parsed:
            try:
                normalized = normalize_order(item)
                order_number = int(normalized["number"])
            except (KeyError, TypeError, ValueError):
                failed += 1
                logger.exception("Failed to normalize parsed order: %s", item)
                continue

            existing_order = db.query(Order).filter(
                Order.number == order_number
            ).first()

            if existing_order:
                logger.info("Updated existing order: %s", order_number)
                existing_order.client = normalized["client"]
                existing_order.value = normalized["value"]
                updated += 1
                continue

            order = Order(
                number=order_number,
                client=normalized["client"],
                value=normalized["value"],
            )

            db.add(order)
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
        raise

    db.refresh(run)

    return {
        "run_id": run.id,
        "status": run.status,
        "message": "Emails processed successfully.",
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

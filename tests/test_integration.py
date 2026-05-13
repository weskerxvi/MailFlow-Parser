import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import Order, ProcessingRun
from app.services.order_pipeline import process_orders_from_email


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    TestingSession = sessionmaker(bind=engine)

    Base.metadata.create_all(bind=engine)

    session = TestingSession()
    yield session
    session.close()


def test_email_processing_pipeline_to_database_flow(session, monkeypatch):
    monkeypatch.setattr(
        "app.services.order_pipeline.email_reader",
        lambda: "Pedido #123 - Cliente Joao - Valor 250",
    )

    result = process_orders_from_email(session)

    order = session.query(Order).first()
    run = session.query(ProcessingRun).first()

    assert result["status"] == "completed"
    assert result["created"] == 1
    assert order.number == 123
    assert order.client == "Joao"
    assert order.value == 250
    assert run.total_parsed == 1

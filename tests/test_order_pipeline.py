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


def test_process_orders_from_email_tracks_created_updated_and_ignored(
    session,
    monkeypatch,
):
    session.add(Order(number=200, client="Old Client", value=10))
    session.commit()

    monkeypatch.setattr(
        "app.services.order_pipeline.email_reader",
        lambda: (
            "Pedido #100 - Cliente New Client - Valor 150\n"
            "Pedido #200 - Cliente Updated Client - Valor 250\n"
            "Invalid line"
        ),
    )

    result = process_orders_from_email(session)

    assert result["status"] == "completed"
    assert result["total_read"] == 3
    assert result["total_parsed"] == 2
    assert result["created"] == 1
    assert result["updated"] == 1
    assert result["ignored"] == 1

    run = session.query(ProcessingRun).first()
    assert run.created == 1
    assert run.updated == 1

    updated_order = session.query(Order).filter(Order.number == 200).first()
    assert updated_order.client == "Updated Client"
    assert updated_order.value == 250

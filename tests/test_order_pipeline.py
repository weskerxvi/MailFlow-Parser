import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import Order, ProcessingRun
from app.services.order_pipeline import process_orders_from_email, process_orders_from_gmail


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


def test_process_orders_from_gmail_uses_gmail_reader(session, monkeypatch):
    monkeypatch.setattr(
        "app.services.order_pipeline.read_gmail_messages",
        lambda: "Pedido #300 - Cliente Gmail Client - Valor R$99,90",
    )

    result = process_orders_from_gmail(session)

    order = session.query(Order).first()

    assert result["source"] == "gmail"
    assert result["created"] == 1
    assert order.number == 300
    assert order.client == "Gmail Client"
    assert order.value == 99.90


def test_process_orders_updates_duplicate_order_inside_same_batch(
    session,
    monkeypatch,
):
    monkeypatch.setattr(
        "app.services.order_pipeline.email_reader",
        lambda: (
            "Pedido #501 - Cliente First Value - Valor 100\n"
            "Pedido #501 - Cliente Latest Value - Valor 200"
        ),
    )

    result = process_orders_from_email(session)

    orders = session.query(Order).all()

    assert result["created"] == 1
    assert result["updated"] == 1
    assert len(orders) == 1
    assert orders[0].number == 501
    assert orders[0].client == "Latest Value"
    assert orders[0].value == 200

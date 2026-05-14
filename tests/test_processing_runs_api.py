import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import Order, ProcessingRun


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSession = sessionmaker(bind=engine)

    Base.metadata.create_all(bind=engine)

    session = TestingSession()
    yield session
    session.close()


@pytest.fixture
def client(session):
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_process_creates_processing_run(client, session, monkeypatch):
    monkeypatch.setattr(
        "app.services.order_pipeline.email_reader",
        lambda: (
            "Pedido #101 - Cliente Ana - Valor 320\n"
            "Pedido #102 - Cliente Bruno - Valor R$450,90\n"
            "Linha invalida"
        ),
    )

    response = client.post("/process")

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "completed"
    assert data["total_read"] == 3
    assert data["total_parsed"] == 2
    assert data["created"] == 2
    assert data["updated"] == 0
    assert data["ignored"] == 1
    assert data["failed"] == 0

    run = session.query(ProcessingRun).first()
    assert run.status == "completed"
    assert run.total_read == 3
    assert run.created == 2

    orders = session.query(Order).all()
    assert len(orders) == 2


def test_process_updates_existing_order_and_tracks_run(client, session, monkeypatch):
    session.add(Order(number=101, client="Ana", value=100))
    session.commit()

    monkeypatch.setattr(
        "app.services.order_pipeline.email_reader",
        lambda: "Pedido #101 - Cliente Ana Maria - Valor 250",
    )

    response = client.post("/process")

    assert response.status_code == 200
    data = response.json()

    assert data["created"] == 0
    assert data["updated"] == 1
    assert data["duplicates"] == 1

    order = session.query(Order).filter(Order.number == 101).first()
    assert order.client == "Ana Maria"
    assert order.value == 250


def test_process_gmail_creates_processing_run(client, session, monkeypatch):
    monkeypatch.setattr(
        "app.services.order_pipeline.read_gmail_messages",
        lambda: "Pedido #201 - Cliente Gmail Buyer - Valor 700",
    )

    response = client.post("/process/gmail")

    assert response.status_code == 200
    data = response.json()

    assert data["source"] == "gmail"
    assert data["created"] == 1
    assert data["total_parsed"] == 1

    order = session.query(Order).first()
    assert order.number == 201
    assert order.client == "Gmail Buyer"


def test_get_processing_runs(client, session):
    session.add(ProcessingRun(status="completed", total_read=1, total_parsed=1))
    session.commit()

    response = client.get("/processing-runs")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["status"] == "completed"


def test_get_processing_run_not_found(client):
    response = client.get("/processing-runs/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Processing run not found."}

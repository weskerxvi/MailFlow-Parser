import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import Order
from app.parser import extract_data
from app.services.process_email import create_order


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    TestingSession = sessionmaker(bind=engine)
 
    Base.metadata.create_all(bind=engine)
 
    session = TestingSession()
    yield session
    session.close()
 
 
def test_parser_to_database_flow(session, monkeypatch):
    def override_session():
        return session
 
    monkeypatch.setattr("app.services.process_email.SessionLocal", override_session)
 
    text = "Pedido #123 - Cliente João - Valor 250"
 
    data = extract_data(text)
    create_order(data)
 
    result = session.query(Order).first()

 
    assert result.number == 123
    assert result.client == "João" 
    assert result.value == "250"
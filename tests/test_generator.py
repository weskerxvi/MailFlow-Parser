import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import Order
from app.reports.generator import get_orders


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    TestingSession = sessionmaker(bind=engine)
 
    Base.metadata.create_all(bind=engine)
 
    session = TestingSession()
    yield session
    session.close()


#####
def test_get_generator(session, monkeypatch):
    def override_session():
        return session
 
    monkeypatch.setattr("app.reports.generator.SessionLocal", override_session)


    order = Order(
        number=123,       
        client="John",   
        value="250"
    )
    
    session.add(order)
    session.commit()
    
    result = get_orders()

    assert result[0].number == 123
    assert result[0].client == "John" 
    assert result[0].value == 250.0
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import Order


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    TestingSession = sessionmaker(bind=engine)
 
    Base.metadata.create_all(bind=engine)
 
    session = TestingSession()
    yield session
    session.close()
 
####
def test_insert_order(session):
    order = Order(
        number=123,       
        client="John",   
        value=250.0
    )
 
    session.add(order)
    session.commit()
 
    result = session.query(Order).first()
 
    assert result.number == 123
    assert result.client == "John" 
    assert result.value == 250.0

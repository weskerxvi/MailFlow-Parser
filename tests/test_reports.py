import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import Order
from app.reports.generator import generate_txt_report, generate_csv_report
from datetime import datetime

import csv


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    TestingSession = sessionmaker(bind=engine)
 
    Base.metadata.create_all(bind=engine)
 
    session = TestingSession()
    yield session
    session.close()


#####
def test_gen_txt(tmp_path, session, monkeypatch):
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

    formated_date = datetime.now().strftime('%d-%m-%Y')

    archive = tmp_path / f"reports-{formated_date}.txt"
    generate_txt_report([order], output_path=tmp_path)

    assert archive.exists()
    assert "Total orders: 1" in archive.read_text()

#####
def test_gen_csv(tmp_path, session, monkeypatch):
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

    formated_date = datetime.now().strftime('%d-%m-%Y')

    archive = tmp_path / f"reports-{formated_date}.csv"
    generate_csv_report([order], output_path=tmp_path)
    open_archive = open(archive, newline="")
    rows = list(csv.reader(open_archive))
    

    assert archive.exists()
    assert ["123", "John", "250"] in rows
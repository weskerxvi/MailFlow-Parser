from sqlalchemy import select

from app.models import Order
from app.database import SessionLocal

from pathlib import Path
from datetime import datetime

import csv

def get_orders():
        try: 
            session = SessionLocal() 
            stmt = select(Order) 
            order_list = session.scalars(stmt).all() 

        finally: 
            session.close() 
        
        return order_list


def generate_txt_report(value, output_path=None):
    if output_path is None:
        path = Path(__file__).parent
    else:
        path = output_path            
    now = datetime.now()

    formated_date = now.strftime('%d-%m-%Y')

    archive = path / f"reports-{formated_date}.txt"
    archive.touch()

    unics = len(set(item.client for item in value))
    
    return archive.write_text("====== ORDERS ======\n" \
    f"Date: {formated_date}\n" \
    f"Total orders: {len(value)}\n" \
    f"Unique customers: {unics}\n")


def generate_csv_report(value, output_path=None):
    if output_path is None:
        path = Path(__file__).parent
    else:
        path = output_path
    now = datetime.now()

    formated_date = now.strftime('%d-%m-%Y')

    archive = path / f"reports-{formated_date}.csv"
    archive.touch()

    list_order = [[item.number, item.client, item.value] for item in value]

    with open(archive, "w", newline="") as f:  
        writing_archive = csv.writer(f)
        writing_archive.writerow(["number", "client", "value"])
        writing_archive.writerows(list_order)

def run():
    orders = get_orders()
    generate_txt_report(orders)
    generate_csv_report(orders)

if __name__ == "__main__":
    run()

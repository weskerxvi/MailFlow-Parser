from app.database import SessionLocal
from app.parser import extract_data
from app.email_reader import email_reader
from app.models  import Order

def create_order(order_list):
    session = SessionLocal()
 
    try:
        for item in order_list:
            order = Order(
                number=int(item["number"]),  
                client=item["client"],
                value=item["value"], 
            )
            session.add(order)
 
        session.commit()
 
    except Exception:
        session.rollback()
        raise
 
    finally:
        session.close()


def run():
    raw_text = email_reader()
    orders = extract_data(raw_text)
    create_order(orders)

if __name__ == "__main__":
    run()

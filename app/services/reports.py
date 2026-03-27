from decimal import Decimal, InvalidOperation

def generate_report(orders):
    total_value = 0
    total_orders = len(orders)
    orders_without_value = 0
    total_value = Decimal("0")

    for order in orders:
        value = order.value  
        
        if value == "SEM VALOR" or not value:
            orders_without_value += 1
            continue
        try:    
            value = value.replace("R$", "").replace(",", ".")
            total_value += Decimal(value)
        except (ValueError, InvalidOperation):
            continue

    return {
        "total_orders": total_orders,
        "total_value": round(float(total_value), 2),
        "orders_without_value": orders_without_value
    }
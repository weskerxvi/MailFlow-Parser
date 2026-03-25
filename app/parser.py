import re

def extract_data(text: str) -> list[dict]:
    match = re.search(
    r'Pedido\s+#(\d+)\s+-\s+Cliente\s+([A-Za-zÀ-ÿ\s]+?)\s+-\s+Valor\s*(.*)',
    text
    )
        
    if not match:
        return None

    number, client, raw_value = match.groups()

    value = re.sub(r"[^\d,\.]", "", raw_value) 
    value = value.replace(",", ".")  

    try:
        value = float(value)
    except:
        return None  

    return {
        "number": int(number),
        "client": client.strip(),
        "value": value
    }
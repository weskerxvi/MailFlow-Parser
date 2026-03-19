import re

def extract_data(text: str) -> list[dict]:
    lines = text.splitlines()
    result = []
    
    for line in lines:
        match = re.search(
                r'Pedido\s+#(\d+)\s+-\s+Cliente\s+([A-Za-zÀ-ÿ\s]+?)\s+-\s+Valor\s*(.*)',
                line
            )
        
        if match:
            id, name, value = match.groups()
            
            value = value.strip()

            if not value:
                value = "SEM VALOR"
            
            
            result.append({'id': id, 'name': name, 'value': value})
        
    return result
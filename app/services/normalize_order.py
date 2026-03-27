from decimal import Decimal

def normalize_order(data: dict) -> dict:
    number = int(data["number"])
    client = data["client"].strip()

    raw_value = data["value"]

    if raw_value == "SEM VALOR" or not raw_value:
        value = "SEM VALOR"
    else:
        value = (
            raw_value
            .replace("R$", "")
            .replace("$", "")
            .replace(",", ".")
            .strip()
        )

        try:
            value = float(value)
        except:
            value = "SEM VALOR"

    return {
        "number": number,
        "client": client,
        "value": value
    }
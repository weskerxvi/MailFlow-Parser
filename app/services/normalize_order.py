from decimal import Decimal

def normalize_order(data: dict) -> dict:
    number = str(data["number"])
    client = data["client"].strip()

    raw_value = data["value"]

    if raw_value == 0 or not raw_value:
        value = 0
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
        except ValueError:
            value = 0

    return {
        "number": number,
        "client": client,
        "value": value
    }
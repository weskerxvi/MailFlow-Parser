from app import extract_data
import pytest

@pytest.mark.parametrize("text, expected", [
    (
        "Pedido #123 - Cliente João - Valor 250",
        [{'number': '123', 'client': 'João', 'value': '250'}]
    ),
    (
        "Pedido #124 - Cliente Maria - Valor",
        [{'number': '124', 'client': 'Maria', 'value': 0}]
    ),
    (
        "Pedido #125 - Cliente Pedro - Valor 300.42",
        [{'number': '125', 'client': 'Pedro', 'value': '300.42'}]
    ),
])
def test_diferent_types_inputs(text, expected):
    result = extract_data(text)
    assert result == expected


@pytest.mark.parametrize("text, expected", [
    (
        "Pedido #564 - Cliente João Azerbub Souza - Valor 250,42",
        [{'number': '564', 'client': 'João Azerbub Souza', 'value': '250,42'}]
    ),
    (
        "Pedido #182 - Cliente Marta Costa silva lima - Valor 23.43",
        [{'number': '182', 'client': 'Marta Costa silva lima', 'value': '23.43'}]
    ),
    (
        "Pedido #243 - Cliente Pedro kelviN àcarno - Valor 300.42",
        [{'number': '243', 'client': 'Pedro kelviN àcarno', 'value': '300.42'}]
    ),
])
def test_name(text, expected):
    result = extract_data(text)
    assert result == expected


@pytest.mark.parametrize("text, expected", [
    (
        "Pedido #0092381092892674 - Cliente João Azerbub - Valor 250,42",
        [{'number': '0092381092892674', 'client': 'João Azerbub', 'value': '250,42'}]
    ),
    (
        "Pedido #111111111 - Cliente Maria - Valor 23.43",
        [{'number': '111111111', 'client': 'Maria', 'value': '23.43'}]
    ),
    (
        "Pedido #199999999999 - Cliente Pedro Akzare - Valor 300.42",
        [{'number': '199999999999', 'client': 'Pedro Akzare', 'value': '300.42'}]
    ),
])
def test_id(text, expected):
    result = extract_data(text)
    assert result == expected


@pytest.mark.parametrize("text, expected", [
    (
        "Pedido #123 - Cliente João - Valor 250,42\n"
        "Pedido #124 - Cliente Maria - Valor R$888664\n"
        "Pedido #125 - Cliente Pedro - Valor $300.42\n"
        "Pedido #443 - Cliente Marlon - Valor R$88.866.423\n"
        "Pedido #125 - Cliente Pedro - Valor R$77,224.242",
        [
            {'number': '123', 'client': 'João', 'value': '250,42'},
            {'number': '124', 'client': 'Maria', 'value': 'R$888664'},
            {'number': '125', 'client': 'Pedro', 'value': '$300.42'},
            {'number': '443', 'client': 'Marlon', 'value': 'R$88.866.423'},
            {'number': '125', 'client': 'Pedro', 'value': 'R$77,224.242'},
        ]
    ),
])

def test_multiple_lines(text, expected):
    result = extract_data(text)
    assert result == expected
import base64

import pytest

from app.exceptions import ConfigurationError
from app.services.gmail_reader import extract_message_body
from app.services.gmail_reader import _load_credentials


def encode_body(text: str) -> str:
    return base64.urlsafe_b64encode(text.encode("utf-8")).decode("utf-8")


def test_extract_message_body_from_plain_text_payload():
    message = {
        "payload": {
            "mimeType": "text/plain",
            "body": {
                "data": encode_body("Pedido #401 - Cliente Mail - Valor 100")
            },
        }
    }

    result = extract_message_body(message)

    assert result == "Pedido #401 - Cliente Mail - Valor 100"


def test_extract_message_body_from_nested_parts():
    message = {
        "payload": {
            "mimeType": "multipart/alternative",
            "parts": [
                {
                    "mimeType": "text/plain",
                    "body": {
                        "data": encode_body("Pedido #402 - Cliente Nested - Valor 200")
                    },
                }
            ],
        }
    }

    result = extract_message_body(message)

    assert result == "Pedido #402 - Cliente Nested - Valor 200"


def test_extract_message_body_prefers_plain_text_over_html():
    message = {
        "payload": {
            "mimeType": "multipart/alternative",
            "parts": [
                {
                    "mimeType": "text/plain",
                    "body": {
                        "data": encode_body("Pedido #403 - Cliente Plain - Valor 300")
                    },
                },
                {
                    "mimeType": "text/html",
                    "body": {
                        "data": encode_body("<p>Pedido #403 - Cliente Plain - Valor 300</p>")
                    },
                },
            ],
        }
    }

    result = extract_message_body(message)

    assert result == "Pedido #403 - Cliente Plain - Valor 300"


def test_load_credentials_raises_when_credentials_are_missing(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setenv("GMAIL_TOKEN_FILE", str(tmp_path / "token.json"))
    monkeypatch.setenv("GMAIL_CREDENTIALS_FILE", str(tmp_path / "credentials.json"))

    with pytest.raises(ConfigurationError):
        _load_credentials()

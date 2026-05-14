import base64
import logging
import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from app.exceptions import ConfigurationError, ExternalServiceError

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

DEFAULT_QUERY = os.getenv("GMAIL_QUERY", "subject:Pedido newer_than:7d")
DEFAULT_MAX_RESULTS = int(os.getenv("GMAIL_MAX_RESULTS", "10"))
USER_ID = "me"
logger = logging.getLogger(__name__)


def get_gmail_service():
    credentials = _load_credentials()
    return build("gmail", "v1", credentials=credentials)


def read_gmail_messages(
    query: str = DEFAULT_QUERY,
    max_results: int = DEFAULT_MAX_RESULTS,
) -> str:
    try:
        service = get_gmail_service()
        response = (
            service.users()
            .messages()
            .list(userId=USER_ID, q=query, maxResults=max_results)
            .execute()
        )
        messages = response.get("messages", [])
        bodies = []

        for message in messages:
            message_data = (
                service.users()
                .messages()
                .get(userId=USER_ID, id=message["id"], format="full")
                .execute()
            )
            body = extract_message_body(message_data)

            if body:
                bodies.append(body)

        logger.info("Fetched %s Gmail messages for query '%s'", len(messages), query)
        return "\n".join(bodies)
    except HttpError as exc:
        logger.exception("Gmail API request failed")
        raise ExternalServiceError("Gmail API request failed.") from exc


def extract_message_body(message_data: dict) -> str:
    payload = message_data.get("payload", {})
    return _extract_text_from_payload(payload)


def _load_credentials() -> Credentials:
    token_path = Path(os.getenv("GMAIL_TOKEN_FILE", "token.json"))
    credentials_path = Path(os.getenv("GMAIL_CREDENTIALS_FILE", "credentials.json"))
    credentials = None

    if not credentials_path.exists() and not token_path.exists():
        raise ConfigurationError("Gmail credentials file was not found.")

    if token_path.exists():
        try:
            credentials = Credentials.from_authorized_user_file(token_path, SCOPES)
        except ValueError as exc:
            raise ConfigurationError("Gmail token file is invalid.") from exc

    if credentials and credentials.valid:
        return credentials

    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    else:
        if not credentials_path.exists():
            raise ConfigurationError("Gmail credentials file was not found.")
        flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
        credentials = flow.run_local_server(port=0)

    token_path.write_text(credentials.to_json())
    return credentials


def _extract_text_from_payload(payload: dict) -> str:
    mime_type = payload.get("mimeType")
    body_data = payload.get("body", {}).get("data")

    if body_data and mime_type in {"text/plain", "text/html"}:
        return _decode_body(body_data)

    parts = payload.get("parts", [])
    plain_texts = []
    fallback_texts = []

    for part in parts:
        part_mime_type = part.get("mimeType")
        text = _extract_text_from_payload(part)

        if not text:
            continue

        if part_mime_type == "text/plain":
            plain_texts.append(text)
        else:
            fallback_texts.append(text)

    if plain_texts:
        return "\n".join(plain_texts)

    return "\n".join(fallback_texts)


def _decode_body(data: str) -> str:
    padding = "=" * (-len(data) % 4)
    decoded = base64.urlsafe_b64decode(data + padding)
    return decoded.decode("utf-8", errors="replace")

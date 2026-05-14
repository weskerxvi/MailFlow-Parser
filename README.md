# MailFlow Parser

MailFlow Parser is a FastAPI backend for processing order data from local email-like text files and Gmail messages. It extracts semi-structured order information, normalizes the data, persists records in PostgreSQL, tracks each processing run, and exposes operational reports through a REST API.

[Live API Docs](https://mailflow-parser.onrender.com/docs)

## Overview

The system receives messages in this format:

```text
Pedido #123 - Cliente Paula - Valor R$764,41
```

It then:

1. reads messages from a local file or Gmail;
2. parses order number, client, and value;
3. normalizes values and client data;
4. creates or updates orders in PostgreSQL;
5. records processing metrics for auditing;
6. exposes orders, reports, and processing history through FastAPI.

## Features

- Local file processing through `emails.txt`
- Gmail processing with the Gmail API and read-only OAuth scope
- Regex-based parsing for semi-structured order messages
- Data normalization before persistence
- PostgreSQL persistence with SQLAlchemy
- Duplicate handling by order number
- Processing run audit history
- TXT and CSV report generation
- Alembic migrations
- Docker and Docker Compose setup
- Structured logging
- JSON error responses
- CI with GitHub Actions
- Automated tests with pytest

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Alembic
- Gmail API
- Docker
- pytest
- GitHub Actions

## Architecture

```text
rpa-email-system/
|-- app/
|   |-- api/
|   |   `-- routes.py
|   |-- reports/
|   |   `-- generator.py
|   |-- services/
|   |   |-- gmail_reader.py
|   |   |-- normalize_order.py
|   |   |-- order_pipeline.py
|   |   `-- reports.py
|   |-- database.py
|   |-- email_reader.py
|   |-- exceptions.py
|   |-- logging_config.py
|   |-- main.py
|   |-- models.py
|   |-- parser.py
|   `-- schemas.py
|-- migrations/
|-- tests/
|-- Dockerfile
|-- docker-compose.yml
|-- alembic.ini
`-- requirements.txt
```

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/process` | Processes local messages from `emails.txt`. |
| `POST` | `/process/gmail` | Fetches matching Gmail messages and processes orders. |
| `GET` | `/orders` | Lists persisted orders. |
| `GET` | `/reports` | Returns aggregate order metrics. |
| `GET` | `/processing-runs` | Lists processing execution history. |
| `GET` | `/processing-runs/{run_id}` | Returns details for one processing run. |

Example `POST /process/gmail` response:

```json
{
  "run_id": 15,
  "status": "completed",
  "message": "Emails processed successfully.",
  "source": "gmail",
  "total_read": 1,
  "total_parsed": 1,
  "created": 0,
  "updated": 1,
  "duplicates": 1,
  "ignored": 0,
  "failed": 0,
  "started_at": "2026-05-14T01:24:45.931336",
  "finished_at": "2026-05-14T01:24:46.136824"
}
```

## Environment Variables

Use `.env.example` as a reference:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/mailflow
DB_ECHO=false
LOG_LEVEL=INFO

GMAIL_QUERY=subject:Pedido newer_than:7d
GMAIL_MAX_RESULTS=10
GMAIL_CREDENTIALS_FILE=credentials.json
GMAIL_TOKEN_FILE=token.json
GMAIL_CREDENTIALS_JSON=
GMAIL_TOKEN_JSON=
```

For hosted environments, prefer `GMAIL_CREDENTIALS_JSON` and `GMAIL_TOKEN_JSON` instead of local credential files.

## Local Setup

Create and activate the virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run migrations:

```powershell
alembic upgrade head
```

Start the API:

```powershell
uvicorn app.main:app --reload
```

Local docs:

```text
http://127.0.0.1:8000/docs
```

## Docker Setup

Start the API and PostgreSQL:

```powershell
docker compose up --build
```

The API container runs migrations before starting Uvicorn:

```text
alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Gmail Setup

The Gmail integration uses this read-only scope:

```text
https://www.googleapis.com/auth/gmail.readonly
```

For local development:

1. Enable the Gmail API in Google Cloud.
2. Create OAuth credentials for a desktop app.
3. Save the OAuth file as `credentials.json`.
4. Run `POST /process/gmail` once to generate `token.json`.

For production:

1. Keep Gmail OAuth secrets out of Git.
2. Store credential and token JSON as environment variables.
3. Configure `GMAIL_CREDENTIALS_JSON` and `GMAIL_TOKEN_JSON` in the host platform.

## Reports

Generate TXT and CSV reports manually:

```powershell
python -m app.reports.generator
```

Generated files are ignored by Git.

## Tests

Run the test suite:

```powershell
pytest
```

Current coverage includes parser behavior, database flow, reports, Gmail body extraction, API endpoints, and processing pipeline behavior.

## Production

The project is deployed on Render:

[https://mailflow-parser.onrender.com/docs](https://mailflow-parser.onrender.com/docs)

Production uses:

- Docker web service
- managed PostgreSQL
- Alembic migrations on startup
- environment-based secrets
- structured application logs

## Engineering Highlights

- Layered architecture with API, services, parser, schemas, reports, and persistence
- Audit trail for each processing execution
- Duplicate-safe order persistence
- External API integration with Gmail
- Schema versioning with Alembic
- Containerized deployment
- CI pipeline with GitHub Actions
- Production deployment with public API documentation

## License

MIT License. See [LICENSE](C:/Users/wsku6/Documents/rpa-email-system/LICENSE).

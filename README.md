# MailFlow Parser

MailFlow Parser is a backend project built with FastAPI to read order data from email-like text, normalize the content, persist the records in PostgreSQL, and expose the results through an API.

The project focuses on backend engineering practices such as:

- text parsing with regex
- data normalization
- REST API design
- SQLAlchemy ORM
- PostgreSQL integration
- automated tests with pytest

## Project Goal

The idea is to simulate a small RPA/email processing workflow.

The application receives semi-structured messages such as:

```text
Pedido #123 - Cliente Paula - Valor R$764,41
```

It then:

1. extracts the relevant order fields
2. normalizes the values
3. stores them in the database
4. exposes the processed data through FastAPI
5. generates summary reports

## Current Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- pytest
- python-dotenv
- Gmail API

## Current Features

- Read raw order data from `emails.txt`
- Read order messages from Gmail through the Gmail API
- Parse orders using regex
- Normalize client and value fields
- Store orders in PostgreSQL
- Prevent duplicate order numbers at database level
- Track each processing run with status and metrics
- List saved orders through the API
- List processing history through the API
- Generate summary data with totals and missing-value count
- Generate TXT and CSV report files

## Project Structure

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
|   |-- init_db.py
|   |-- main.py
|   |-- models.py
|   |-- parser.py
|   `-- schemas.py
|-- tests/
|-- emails.txt
|-- requirements.txt
`-- .env
```

## How The Flow Works

### 1. Read input

The application can read text from `emails.txt` through [email_reader.py](C:/Users/wsku6/Documents/rpa-email-system/app/email_reader.py) or fetch matching messages from Gmail through [gmail_reader.py](C:/Users/wsku6/Documents/rpa-email-system/app/services/gmail_reader.py).

### 2. Parse the message

The parser in [parser.py](C:/Users/wsku6/Documents/rpa-email-system/app/parser.py) uses regex to extract:

- order number
- client name
- order value

### 3. Normalize the data

The service in [normalize_order.py](C:/Users/wsku6/Documents/rpa-email-system/app/services/normalize_order.py) cleans and standardizes the extracted values before saving them.

### 4. Run the processing pipeline

The pipeline in [order_pipeline.py](C:/Users/wsku6/Documents/rpa-email-system/app/services/order_pipeline.py) orchestrates parsing, normalization, persistence, duplicate handling, and processing run metrics.

### 5. Persist in PostgreSQL

The database connection is configured in [database.py](C:/Users/wsku6/Documents/rpa-email-system/app/database.py), and the order model is defined in [models.py](C:/Users/wsku6/Documents/rpa-email-system/app/models.py).

### 6. Expose the results

The routes in [routes.py](C:/Users/wsku6/Documents/rpa-email-system/app/api/routes.py) allow the user to:

- process the local email file
- process matching Gmail messages
- list stored orders
- inspect processing history
- get a report summary

### 7. Track processing runs

Every execution of `POST /process` creates a processing run with:

- status
- total lines read
- total parsed orders
- created orders
- updated existing orders
- ignored lines
- failed items
- start and finish timestamps

### 8. Generate report files

[generator.py](C:/Users/wsku6/Documents/rpa-email-system/app/reports/generator.py) creates TXT and CSV files based on the stored orders.

## Environment Variables

Create a `.env` file in the root of the project:

```env
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/mailflow
DB_ECHO=false
GMAIL_QUERY=subject:Pedido newer_than:7d
GMAIL_MAX_RESULTS=10
GMAIL_CREDENTIALS_FILE=credentials.json
GMAIL_TOKEN_FILE=token.json
```

Gmail credentials are intentionally loaded from local files and must not be committed to the repository.

## PostgreSQL Setup

Make sure PostgreSQL is running locally and create the database:

```sql
CREATE DATABASE mailflow;
```

Then initialize the tables:

```powershell
python -m app.init_db
```

## Local Setup

### 1. Create the virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Start the API

```powershell
uvicorn app.main:app --reload
```

Available URLs:

- `http://127.0.0.1:8000`
- `http://127.0.0.1:8000/docs`

## Example Input

Place sample content inside `emails.txt`:

```text
Pedido #101 - Cliente Ana - Valor 320
Pedido #102 - Cliente Bruno - Valor R$450,90
Pedido #103 - Cliente Carla - Valor
```

## API Endpoints

### `POST /process`

Reads `emails.txt`, parses the entries, normalizes the data, and stores the orders in the database.

Example response:

```json
{
  "run_id": 15,
  "status": "completed",
  "message": "Emails processed successfully.",
  "total_read": 3,
  "total_parsed": 2,
  "created": 2,
  "updated": 1,
  "duplicates": 1,
  "ignored": 1,
  "failed": 0,
  "started_at": "2026-05-13T10:00:00",
  "finished_at": "2026-05-13T10:00:01"
}
```

### `POST /process/gmail`

Fetches matching Gmail messages, extracts their text content, parses orders, and stores the results in the database.

The Gmail reader uses the read-only Gmail scope:

```text
https://www.googleapis.com/auth/gmail.readonly
```

Before running this endpoint, create OAuth credentials in Google Cloud, enable the Gmail API, and place the downloaded OAuth client file at the path configured by `GMAIL_CREDENTIALS_FILE`.

### `GET /orders`

Returns all saved orders.

### `GET /reports`

Returns a summary with:

- total number of orders
- total order value
- number of orders without value

### `GET /processing-runs`

Returns the history of processing executions.

### `GET /processing-runs/{run_id}`

Returns the metrics and status of a specific processing execution.

## Report Files

To generate TXT and CSV reports manually:

```powershell
python -m app.reports.generator
```

The files are generated based on the records already stored in the database.

## Running Tests

```powershell
pytest
```

## Engineering Highlights

This project demonstrates backend practices such as:

- API development with FastAPI
- ORM-based persistence with SQLAlchemy
- PostgreSQL-ready database configuration
- layered architecture with API, services, parser, schemas, and reports
- external API integration with Gmail
- semi-structured data parsing and normalization
- duplicate handling and update behavior for existing orders
- processing audit trail with execution status and metrics
- automated tests covering parser, reports, database flow, API endpoints, and pipeline behavior

## License

MIT License. See [LICENSE](C:/Users/wsku6/Documents/rpa-email-system/LICENSE).

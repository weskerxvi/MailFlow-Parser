# MailFlow Parser

MailFlow Parser is a backend project built with FastAPI to read order data from email-like text, normalize the content, persist the records in PostgreSQL, and expose the results through an API.

The project was created as a portfolio piece focused on backend fundamentals:

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

## Current Features

- Read raw order data from `emails.txt`
- Parse orders using regex
- Normalize client and value fields
- Store orders in PostgreSQL
- Prevent duplicate order numbers at database level
- List saved orders through the API
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
|   |   |-- normalize_order.py
|   |   |-- process_email.py
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

The application reads text from `emails.txt` through [email_reader.py](C:/Users/wsku6/Documents/rpa-email-system/app/email_reader.py).

### 2. Parse the message

The parser in [parser.py](C:/Users/wsku6/Documents/rpa-email-system/app/parser.py) uses regex to extract:

- order number
- client name
- order value

### 3. Normalize the data

The service in [normalize_order.py](C:/Users/wsku6/Documents/rpa-email-system/app/services/normalize_order.py) cleans and standardizes the extracted values before saving them.

### 4. Persist in PostgreSQL

The database connection is configured in [database.py](C:/Users/wsku6/Documents/rpa-email-system/app/database.py), and the order model is defined in [models.py](C:/Users/wsku6/Documents/rpa-email-system/app/models.py).

### 5. Expose the results

The routes in [routes.py](C:/Users/wsku6/Documents/rpa-email-system/app/api/routes.py) allow the user to:

- process the local email file
- list stored orders
- get a report summary

### 6. Generate report files

[generator.py](C:/Users/wsku6/Documents/rpa-email-system/app/reports/generator.py) creates TXT and CSV files based on the stored orders.

## Environment Variables

Create a `.env` file in the root of the project:

```env
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/mailflow
DB_ECHO=false
```

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
  "message": "Emails processed successfully.",
  "created": 2,
  "duplicates": 1
}
```

### `GET /orders`

Returns all saved orders.

### `GET /reports`

Returns a summary with:

- total number of orders
- total order value
- number of orders without value

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

## Notes About Gmail

The project is being prepared for Gmail integration, but Gmail processing is not active in the current application flow yet.

The Gmail-related packages are already present in the project dependencies for the next implementation step.

## Why This Project Is Useful For Portfolio

This project shows practical backend skills such as:

- building APIs with FastAPI
- using SQLAlchemy with PostgreSQL
- parsing and transforming semi-structured data
- organizing code into layers
- creating unit and integration tests
- thinking about future integrations and scalability

## Next Improvements

- Gmail API integration
- better API response schemas
- structured logging
- Alembic migrations
- stronger validation with Pydantic
- API tests with FastAPI `TestClient`
- improved error handling

## License

MIT License. See [LICENSE](C:/Users/wsku6/Documents/rpa-email-system/LICENSE).

# 📬 MailFlow Parser

A simple API and automation system to read text-based emails, extract order data, normalize it, and store the results in a SQLite database.

> ⚠️ **Note:** This project is a **Minimum Viable Product (MVP)** and is currently under active development. Planned improvements include PostgreSQL integration, Gmail API integration, and API enhancements.

---

## 📌 Project Objective

This project simulates a small RPA/email processing system.

The goal is to take semi-structured input (emails), extract relevant order data, and transform it into structured records for querying and reporting.

### Example input:

```text
Pedido #123 - Cliente Paula - Valor R$764,41
```

---

## 🚀 Tech Stack

- Python  
- FastAPI  
- SQLAlchemy  
- SQLite  
- Pydantic  
- pytest  
- Regex  

---

## ⚙️ How It Works

1. The system reads data from the `emails.txt` file  
2. A parser extracts data using regex  
3. The extracted data is normalized  
4. Orders are stored in the `rpa.db` database  
5. The API exposes endpoints for querying and reporting  
6. Reports can be generated in `.txt` and `.csv`  

---

## 🗂️ Project Structure

```text
rpa-email-system/
│-- app/
│   │-- api/
│   │   └── routes.py
│   │-- reports/
│   │   └── generator.py
│   │-- services/
│   │   │-- normalize_order.py
│   │   │-- process_email.py
│   │   └── reports.py
│   │-- database.py
│   │-- email_reader.py
│   │-- main.py
│   │-- models.py
│   │-- parser.py
│   │-- init_db.py
│   │-- parser.py
│   └── schemas.py
│-- tests/
│-- emails.txt
│-- requirements.txt
└── rpa.db
```

---

## ▶️ Running Locally

### 1. Create and activate a virtual environment

```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Start the API

```bash
uvicorn app.main:app --reload
```

Access:

- http://127.0.0.1:8000  
- http://127.0.0.1:8000/docs  

---

## 📥 Usage

Add lines to `emails.txt`:

```text
Pedido #123 - Cliente John Doe - Valor 250
Pedido #124 - Cliente Maria Souza - Valor R$320.90
Pedido #125 - Cliente Pedro Lima - Valor
```

---

## 🔗 Endpoints

### `POST /process`

Processes the emails and stores valid orders.

```json
{
  "message": "Emails processed successfully.",
  "created": 2,
  "duplicates": 1
}
```

---

### `GET /orders`

Returns all stored orders.

---

### `GET /reports`

Returns:

- total number of orders  
- total value  
- number of orders without value  

---

## 📊 Reports

Generate reports manually:

```bash
python -m app.reports.generator
```

Generated files:

- `reports-dd-mm-yyyy.txt`  
- `reports-dd-mm-yyyy.csv`  

---

## 🧪 Running Tests

```bash
pytest
```

---

## 🛠️ Roadmap

This project is evolving beyond the MVP. Planned improvements:

- PostgreSQL integration  
- Gmail API integration  
- Improved validation with Pydantic  
- Environment-based configuration  
- Structured logging  
- Database migrations with Alembic  
- Improved API design  
- Better test coverage  

---

## 📄 License

MIT License. See the `LICENSE` file for details.
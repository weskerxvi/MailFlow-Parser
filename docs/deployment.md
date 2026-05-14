# Deployment Notes

The project is deployed on Render as a Docker web service with a managed PostgreSQL database.

## Production URL

```text
https://mailflow-parser.onrender.com/docs
```

## Render Setup

1. Create a PostgreSQL database on Render.
2. Create a Web Service connected to the GitHub repository.
3. Use the `main` branch.
4. Select Docker runtime.
5. Configure environment variables.
6. Deploy.

## Required Environment Variables

```env
DATABASE_URL=postgresql+psycopg2://USER:PASSWORD@HOST:PORT/DATABASE
DB_ECHO=false
LOG_LEVEL=INFO
GMAIL_QUERY=subject:Pedido newer_than:7d
GMAIL_MAX_RESULTS=10
GMAIL_CREDENTIALS_JSON={...}
GMAIL_TOKEN_JSON={...}
```

## Startup

The Docker command runs migrations before starting the API:

```text
alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Notes

- Do not commit `.env`, `credentials.json`, or `token.json`.
- Use Render environment variables for production secrets.
- Prefer the internal Render PostgreSQL URL when the API and database are in the same Render account.

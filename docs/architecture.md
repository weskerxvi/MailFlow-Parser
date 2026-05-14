# Architecture Notes

MailFlow Parser is organized around a small processing pipeline.

## Flow

```text
Input source
  -> parser
  -> normalization
  -> order persistence
  -> processing run audit
  -> API/report output
```

## Layers

- `app/api`: FastAPI routes and HTTP entrypoints.
- `app/services`: business logic, Gmail reader, normalization, reports, and processing pipeline.
- `app/parser.py`: regex-based extraction for semi-structured messages.
- `app/models.py`: SQLAlchemy database models.
- `app/schemas.py`: Pydantic response schemas.
- `migrations`: Alembic database schema versioning.
- `tests`: automated tests for parser, services, reports, API, and Gmail body extraction.

## Processing Runs

Every execution creates a `ProcessingRun` record with:

- status
- source
- total lines read
- total parsed orders
- created orders
- updated orders
- ignored lines
- failed items
- timestamps

This gives the project an audit trail instead of only returning transient API responses.

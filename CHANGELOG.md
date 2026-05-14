# Changelog

## v1.0.0

- Added FastAPI endpoints for processing local and Gmail order messages.
- Added SQLAlchemy models for orders and processing run audit history.
- Added Gmail API integration with read-only OAuth scope.
- Added duplicate handling inside each processing batch.
- Added TXT and CSV report generation.
- Added Alembic migrations.
- Added Docker and Docker Compose setup.
- Added structured logging and JSON error responses.
- Added automated tests for parser, reports, database flow, API endpoints, Gmail body extraction, and processing pipeline behavior.

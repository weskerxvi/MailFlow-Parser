import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.exceptions import AppError
from app.logging_config import configure_logging

configure_logging()

logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(router)


@app.exception_handler(AppError)
def handle_app_error(request: Request, exc: AppError):
    logger.warning(
        "Application error on %s %s: %s",
        request.method,
        request.url.path,
        exc.message,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message, "code": exc.code},
    )


@app.exception_handler(Exception)
def handle_unexpected_error(request: Request, exc: Exception):
    logger.exception(
        "Unexpected error on %s %s",
        request.method,
        request.url.path,
    )
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Unexpected internal error.",
            "code": "internal_error",
        },
    )

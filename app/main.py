from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from app.api.exception_handlers import (
    request_validation_error_handler,
    validation_error_handler,
)
from app.api.v1.routers.user_router import router as user_router

app = FastAPI(title="Financeiro API")

app.add_exception_handler(RequestValidationError, request_validation_error_handler)
app.add_exception_handler(ValidationError, validation_error_handler)
app.include_router(user_router, prefix="/api/v1")

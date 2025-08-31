# app/exceptions/handlers.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions.custom_exceptions import FileTooLargeError, InvalidFileTypeError


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(FileTooLargeError)
    async def file_too_large_handler(request: Request, exc: FileTooLargeError):
        return JSONResponse(
            status_code=413,
            content={"message": exc.message},
        )

    @app.exception_handler(InvalidFileTypeError)
    async def invalid_file_type_handler(request: Request, exc: InvalidFileTypeError):
        return JSONResponse(
            status_code=400,
            content={"message": exc.message},
        )

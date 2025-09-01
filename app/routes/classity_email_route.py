from fastapi import APIRouter, UploadFile, File, Form

from app.exceptions.custom_exceptions import FileTooLargeError, InvalidFileTypeError
from app.schemas.email_schema import FileResponseDTO, TextResponseDTO
from app.services.classity_email_service import EmailClassificationService
from fastapi.middleware.cors import CORSMiddleware
router = APIRouter(prefix="/classity-email", tags=["Email Classification"])





allowed_types = ["application/pdf", "text/plain"]
max_size = 1_000_000  # 1 MB

# Instanciando o serviço uma única vez
service = EmailClassificationService()


@router.post("/file", response_model=FileResponseDTO)
async def classity_file(file: UploadFile = File(...)):
    content = await file.read()
    size_content = len(content)
    content_type = file.content_type

    if content_type not in allowed_types:
        raise InvalidFileTypeError(content_type, allowed_types)
    if size_content >= max_size:
        raise FileTooLargeError(size_content, max_size)

    # Convertendo conteúdo para texto
    text = content.decode("utf-8", errors="ignore")

    # Chamando o serviço de classificação
    result = service.classify_email(text)

    return FileResponseDTO(filename=file.filename, length=size_content, classification=result)


@router.post("/text", response_model=TextResponseDTO)
async def classity_text(text: str = Form(...)):
    content = text.encode("utf-8")
    size_content = len(content)
    content_type = "text/plain"

    if content_type not in allowed_types:
        raise InvalidFileTypeError(content_type, allowed_types)
    if size_content >= max_size:
        raise FileTooLargeError(size_content, max_size)

    # Chamando o serviço de classificação
    result = service.classify_email(text)

    return TextResponseDTO(
        text_length=size_content,
        text_preview=text[:50] + ("..." if len(text) > 50 else ""),
        classification=result
    )

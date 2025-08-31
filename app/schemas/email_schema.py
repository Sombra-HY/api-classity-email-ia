from pydantic import BaseModel

class FileResponseDTO(BaseModel):
    filename: str
    length: int
    classification: str

class TextResponseDTO(BaseModel):
    text_length: int
    text_preview: str
    classification: str

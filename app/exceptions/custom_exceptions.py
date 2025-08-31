class FileTooLargeError(Exception):
    """Exceção lançada quando o arquivo enviado excede o tamanho máximo permitido."""
    def __init__(self, size: int, max_size: int):
        self.size = size
        self.max_size = max_size
        self.status_code =413
        self.message = f"Arquivo muito grande ({size} bytes). Máximo permitido: {max_size} bytes."
        super().__init__(self.message)

class InvalidFileTypeError(Exception):
    """Exceção lançada quando o arquivo enviado não é do tipo permitido."""
    def __init__(self, content_type: str, allowed_types: list[str]):
        self.content_type = content_type
        self.allowed_types = allowed_types
        self.status_code =400
        self.message = f"Tipo de arquivo '{content_type}' não permitido. Tipos permitidos: {allowed_types}"
        super().__init__(self.message)
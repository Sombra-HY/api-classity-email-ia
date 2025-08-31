from fastapi import FastAPI
from app.exceptions.handlers import register_exception_handlers
from app.routes.classity_email_route import router  # sua rota de upload

app = FastAPI()

# Registrar handlers de exceções
register_exception_handlers(app)

# Registrar rotas
app.include_router(router)

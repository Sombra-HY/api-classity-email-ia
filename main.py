from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.exceptions.handlers import register_exception_handlers
from app.routes.classity_email_route import router  # sua rota de upload

app = FastAPI()

# Habilita CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # permite todas as origens (em produção, use seu domínio específico)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Registrar handlers de exceções
register_exception_handlers(app)

# Registrar rotas
app.include_router(router)

from pydantic import BaseModel
from typing import Optional


# =============================
# Usuário
# =============================
class UsuarioBase(BaseModel):
    nome: str
    email: str
    motorista: bool = False


class UsuarioCreate(UsuarioBase):
    senha: str


class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        orm_mode = True


# =============================
# Corrida
# =============================
class CorridaBase(BaseModel):
    origem: str
    destino: str
    forma_pagamento: str


class CorridaCreate(CorridaBase):
    pass


class CorridaResponse(CorridaBase):
    id: int
    status: str
    preco: float
    passageiro_id: int
    motorista_id: Optional[int] = None

    class Config:
        orm_mode = True


# =============================
# Avaliação
# =============================
class AvaliacaoBase(BaseModel):
    nota: int
    comentario: Optional[str] = None


class AvaliacaoCreate(AvaliacaoBase):
    pass


class AvaliacaoResponse(AvaliacaoBase):
    id: int
    corrida_id: int
    avaliador_id: int
    avaliado_id: int

    class Config:
        orm_mode = True


# =============================
# Autenticação
# =============================
class Token(BaseModel):
    access_token: str
    token_type: str


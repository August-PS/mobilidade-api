from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)
    motorista = Column(Boolean, default=False)  # True = motorista, False = passageiro

    # Relacionamentos
    corridas_passageiro = relationship(
        "Corrida",
        back_populates="passageiro",
        foreign_keys="Corrida.passageiro_id"
    )
    corridas_motorista = relationship(
        "Corrida",
        back_populates="motorista_usuario",
        foreign_keys="Corrida.motorista_id"
    )
    avaliacoes_recebidas = relationship(
        "Avaliacao",
        back_populates="avaliado",
        foreign_keys="Avaliacao.avaliado_id"
    )
    avaliacoes_feitas = relationship(
        "Avaliacao",
        back_populates="avaliador",
        foreign_keys="Avaliacao.avaliador_id"
    )


class Corrida(Base):
    __tablename__ = "corridas"

    id = Column(Integer, primary_key=True, index=True)
    origem = Column(String, nullable=False)
    destino = Column(String, nullable=False)
    status = Column(String, default="pendente")  # pendente, em_andamento, concluida
    preco = Column(Float, nullable=False)
    forma_pagamento = Column(String, nullable=False)  # dinheiro, cartão, pix
    criado_em = Column(DateTime, default=datetime.utcnow)

    passageiro_id = Column(Integer, ForeignKey("usuarios.id"))
    motorista_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)

    # Relacionamentos
    passageiro = relationship(
        "Usuario",
        back_populates="corridas_passageiro",
        foreign_keys=[passageiro_id]
    )
    motorista_usuario = relationship(
        "Usuario",
        back_populates="corridas_motorista",
        foreign_keys=[motorista_id]
    )
    avaliacoes = relationship("Avaliacao", back_populates="corrida")


class Avaliacao(Base):
    __tablename__ = "avaliacoes"

    id = Column(Integer, primary_key=True, index=True)
    nota = Column(Integer, nullable=False)  # 1 a 5
    comentario = Column(String, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)

    corrida_id = Column(Integer, ForeignKey("corridas.id"))
    avaliador_id = Column(Integer, ForeignKey("usuarios.id"))
    avaliado_id = Column(Integer, ForeignKey("usuarios.id"))

    # Relacionamentos
    corrida = relationship("Corrida", back_populates="avaliacoes")
    avaliador = relationship("Usuario", back_populates="avaliacoes_feitas", foreign_keys=[avaliador_id])
    avaliado = relationship("Usuario", back_populates="avaliacoes_recebidas", foreign_keys=[avaliado_id])

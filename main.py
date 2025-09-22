from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models, schemas
from auth import gerar_hash_senha, verificar_senha, criar_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import random

# Criar tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependência para abrir/fechar sessão
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================
# 👤 ROTAS DE USUÁRIO + LOGIN
# ============================================================

@app.post("/usuarios/", response_model=schemas.UsuarioResponse)
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    novo_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=gerar_hash_senha(usuario.senha),
        motorista=usuario.motorista
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario


@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == form_data.username).first()
    if not usuario or not verificar_senha(form_data.password, usuario.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    access_token_expires = timedelta(minutes=30)
    token = criar_access_token(
        data={"sub": usuario.email}, expires_delta=access_token_expires
    )
    return {"access_token": token, "token_type": "bearer"}


@app.get("/meu-perfil")
def meu_perfil(usuario: models.Usuario = Depends(get_current_user)):
    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "motorista": usuario.motorista
    }


@app.get("/motorista-area")
def area_motorista(usuario: models.Usuario = Depends(get_current_user)):
    if not usuario.motorista:
        raise HTTPException(status_code=403, detail="Acesso permitido apenas para motoristas")
    return {"mensagem": f"Bem-vindo, motorista {usuario.nome}!"}


@app.get("/passageiro-area")
def area_passageiro(usuario: models.Usuario = Depends(get_current_user)):
    if usuario.motorista:
        raise HTTPException(status_code=403, detail="Acesso permitido apenas para passageiros")
    return {"mensagem": f"Bem-vindo, passageiro {usuario.nome}!"}


# ============================================================
# 🚖 ROTAS DE CORRIDAS
# ============================================================

# Passageiro solicita corrida
@app.post("/corridas/", response_model=schemas.CorridaResponse)
def solicitar_corrida(corrida: schemas.CorridaCreate, 
                      db: Session = Depends(get_db), 
                      usuario: models.Usuario = Depends(get_current_user)):
    if usuario.motorista:
        raise HTTPException(status_code=403, detail="Apenas passageiros podem solicitar corridas")
    
    preco = round(random.uniform(15, 80), 2)  # preço aleatório entre 15 e 80

    nova_corrida = models.Corrida(
        origem=corrida.origem,
        destino=corrida.destino,
        forma_pagamento=corrida.forma_pagamento,
        preco=preco,
        passageiro_id=usuario.id
    )
    db.add(nova_corrida)
    db.commit()
    db.refresh(nova_corrida)
    return nova_corrida


# Motorista visualiza corridas pendentes
@app.get("/corridas/pendentes", response_model=list[schemas.CorridaResponse])
def listar_corridas_pendentes(db: Session = Depends(get_db), 
                              usuario: models.Usuario = Depends(get_current_user)):
    if not usuario.motorista:
        raise HTTPException(status_code=403, detail="Apenas motoristas podem ver corridas pendentes")
    
    return db.query(models.Corrida).filter(models.Corrida.status == "pendente").all()


# Passageiro lista todas as suas corridas (histórico)
@app.get("/corridas/minhas", response_model=list[schemas.CorridaResponse])
def minhas_corridas(db: Session = Depends(get_db),
                    usuario: models.Usuario = Depends(get_current_user)):

    if usuario.motorista:
        raise HTTPException(status_code=403, detail="Apenas passageiros podem ver suas corridas")

    return db.query(models.Corrida).filter(models.Corrida.passageiro_id == usuario.id).all()


# Motorista lista todas as corridas que já aceitou/finalizou (histórico)
@app.get("/corridas/motorista", response_model=list[schemas.CorridaResponse])
def corridas_motorista(db: Session = Depends(get_db),
                       usuario: models.Usuario = Depends(get_current_user)):

    if not usuario.motorista:
        raise HTTPException(status_code=403, detail="Apenas motoristas podem ver suas corridas")

    return db.query(models.Corrida).filter(models.Corrida.motorista_id == usuario.id).all()


# Motorista aceita corrida
@app.put("/corridas/{corrida_id}/aceitar", response_model=schemas.CorridaResponse)
def aceitar_corrida(corrida_id: int, db: Session = Depends(get_db),
                    usuario: models.Usuario = Depends(get_current_user)):

    if not usuario.motorista:
        raise HTTPException(status_code=403, detail="Apenas motoristas podem aceitar corridas")

    corrida = db.query(models.Corrida).filter(models.Corrida.id == corrida_id).first()
    if not corrida:
        raise HTTPException(status_code=404, detail="Corrida não encontrada")
    if corrida.status != "pendente":
        raise HTTPException(status_code=400, detail="Corrida já foi aceita ou concluída")

    corrida.status = "em_andamento"
    corrida.motorista_id = usuario.id
    db.commit()
    db.refresh(corrida)

    return corrida


# Motorista finaliza corrida
@app.put("/corridas/{corrida_id}/finalizar", response_model=schemas.CorridaResponse)
def finalizar_corrida(corrida_id: int, db: Session = Depends(get_db),
                      usuario: models.Usuario = Depends(get_current_user)):

    if not usuario.motorista:
        raise HTTPException(status_code=403, detail="Apenas motoristas podem finalizar corridas")

    corrida = db.query(models.Corrida).filter(models.Corrida.id == corrida_id).first()
    if not corrida:
        raise HTTPException(status_code=404, detail="Corrida não encontrada")
    if corrida.motorista_id != usuario.id:
        raise HTTPException(status_code=403, detail="Você não é o motorista desta corrida")
    if corrida.status != "em_andamento":
        raise HTTPException(status_code=400, detail="Só é possível finalizar corridas em andamento")

    corrida.status = "concluida"
    db.commit()
    db.refresh(corrida)

    return corrida


# Passageiro consulta o status da corrida
@app.get("/corridas/{corrida_id}", response_model=schemas.CorridaResponse)
def obter_corrida(corrida_id: int,
                  db: Session = Depends(get_db),
                  usuario: models.Usuario = Depends(get_current_user)):

    corrida = db.query(models.Corrida).filter(models.Corrida.id == corrida_id).first()
    if not corrida:
        raise HTTPException(status_code=404, detail="Corrida não encontrada")

    # Garante que só o passageiro dono ou o motorista designado podem consultar
    if corrida.passageiro_id != usuario.id and corrida.motorista_id != usuario.id:
        raise HTTPException(status_code=403, detail="Você não tem acesso a esta corrida")

    return corrida

# Passageiro ou motorista avalia após corrida concluída
@app.post("/avaliacoes/{corrida_id}", response_model=schemas.AvaliacaoResponse)
def avaliar_usuario(corrida_id: int, avaliacao: schemas.AvaliacaoCreate,
                    db: Session = Depends(get_db),
                    usuario: models.Usuario = Depends(get_current_user)):

    corrida = db.query(models.Corrida).filter(models.Corrida.id == corrida_id).first()
    if not corrida:
        raise HTTPException(status_code=404, detail="Corrida não encontrada")

    if corrida.status != "concluida":
        raise HTTPException(status_code=400, detail="Só é possível avaliar corridas concluídas")

    # passageiro avalia motorista
    if usuario.id == corrida.passageiro_id:
        avaliado_id = corrida.motorista_id
    # motorista avalia passageiro
    elif usuario.id == corrida.motorista_id:
        avaliado_id = corrida.passageiro_id
    else:
        raise HTTPException(status_code=403, detail="Você não participou desta corrida")

    if not avaliado_id:
        raise HTTPException(status_code=400, detail="Não há usuário para avaliar")

    nova_avaliacao = models.Avaliacao(
        nota=avaliacao.nota,
        comentario=avaliacao.comentario,
        corrida_id=corrida.id,
        avaliador_id=usuario.id,
        avaliado_id=avaliado_id
    )

    db.add(nova_avaliacao)
    db.commit()
    db.refresh(nova_avaliacao)

    return nova_avaliacao


# Consultar avaliações de um usuário
@app.get("/usuarios/{usuario_id}/avaliacoes", response_model=list[schemas.AvaliacaoResponse])
def listar_avaliacoes(usuario_id: int, db: Session = Depends(get_db)):
    return db.query(models.Avaliacao).filter(models.Avaliacao.avaliado_id == usuario_id).all()


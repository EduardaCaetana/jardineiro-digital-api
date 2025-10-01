# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from . import models, schemas
from .database import engine, SessionLocal

# --- LÓGICA DE SEEDING (Banco Pré-Cadastrado SEM FOTO) ---
def seed_db():
    db = SessionLocal()
    try:
        if db.query(models.Planta).count() == 0:
            print("Enciclopédia vazia. Semeando com dados iniciais...")
            plantas_iniciais = [
                models.Planta(nome_popular="Jiboia", nome_cientifico="Epipremnum aureum", familia="Araceae", origem="Ilhas Salomão", cuidados="Manter o solo úmido, mas não encharcado. Gosta de luz indireta. Tóxica para pets."),
                models.Planta(nome_popular="Espada-de-São-Jorge", nome_cientifico="Dracaena trifasciata", familia="Asparagaceae", origem="África", cuidados="Muito resistente. Regar apenas quando o solo estiver bem seco. Purifica o ar."),
                models.Planta(nome_popular="Costela-de-Adão", nome_cientifico="Monstera deliciosa", familia="Araceae", origem="México", cuidados="Luz indireta e solo levemente úmido. Limpar as folhas com um pano úmido para remover poeira."),
                models.Planta(nome_popular="Suculenta Orelha-de-Shrek", nome_cientifico="Crassula ovata 'Gollum'", familia="Crassulaceae", origem="África do Sul", cuidados="Ama sol pleno e pouquíssima água. Deixar o solo secar completamente entre as regas."),
                models.Planta(nome_popular="Samambaia", nome_cientifico="Nephrolepis exaltata", familia="Lomariopsidaceae", origem="Regiões tropicais", cuidados="Gosta de muita umidade e sombra. Borrife água nas folhas regularmente e mantenha o solo sempre úmido.")
            ]
            db.add_all(plantas_iniciais)
            db.commit()
            print("Semeadura completa.")
        else:
            print("Enciclopédia já contém dados. Semeadura ignorada.")
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)
seed_db()
# --- FIM DA LÓGICA DE SEEDING ---

app = FastAPI(title="Enciclopédia Botânica Colaborativa API")

# Bloco do CORS
origins = ["http://127.0.0.1:5500", "null"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Função get_db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ENDPOINTS PÚBLICOS (NÃO MUDAM) ---
@app.post("/plantas/", response_model=schemas.Planta, status_code=201, tags=["Enciclopédia"])
def create_planta(planta: schemas.PlantaCreate, db: Session = Depends(get_db)):
    db_planta = models.Planta(**planta.model_dump())
    db.add(db_planta)
    db.commit()
    db.refresh(db_planta)
    return db_planta

@app.get("/plantas/", response_model=List[schemas.Planta], tags=["Enciclopédia"])
def read_plantas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    plantas = db.query(models.Planta).order_by(models.Planta.id).offset(skip).limit(limit).all()
    return plantas

# ... (o resto dos endpoints GET por ID, PUT e DELETE continuam exatamente iguais) ...
@app.get("/plantas/{planta_id}", response_model=schemas.Planta, tags=["Enciclopédia"])
def read_planta(planta_id: int, db: Session = Depends(get_db)):
    db_planta = db.query(models.Planta).filter(models.Planta.id == planta_id).first()
    if db_planta is None:
        raise HTTPException(status_code=404, detail="Planta não encontrada na enciclopédia")
    return db_planta

@app.put("/plantas/{planta_id}", response_model=schemas.Planta, tags=["Enciclopédia"])
def update_planta(planta_id: int, planta_update: schemas.PlantaUpdate, db: Session = Depends(get_db)):
    db_planta = db.query(models.Planta).filter(models.Planta.id == planta_id).first()
    if db_planta is None:
        raise HTTPException(status_code=404, detail="Planta não encontrada na enciclopédia")
    
    update_data = planta_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_planta, key, value)
        
    db.commit()
    db.refresh(db_planta)
    return db_planta

@app.delete("/plantas/{planta_id}", response_model=schemas.Planta, tags=["Enciclopédia"])
def delete_planta(planta_id: int, db: Session = Depends(get_db)):
    db_planta = db.query(models.Planta).filter(models.Planta.id == planta_id).first()
    if db_planta is None:
        raise HTTPException(status_code=404, detail="Planta não encontrada na enciclopédia")
    db.delete(db_planta)
    db.commit()
    return db_planta
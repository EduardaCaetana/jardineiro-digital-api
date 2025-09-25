# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from . import crud, models, schemas
from .database import engine, get_db, AsyncSessionLocal
import datetime

# Função para popular o banco com algumas espécies iniciais
async def popular_banco():
    async with AsyncSessionLocal() as db:
        especies_iniciais = [
            {"nome_popular": "Jiboia", "nome_cientifico": "Epipremnum aureum", "instrucoes_de_cuidado": "Manter o solo úmido, mas não encharcado. Gosta de luz indireta.", "frequencia_rega_dias": 7},
            {"nome_popular": "Espada-de-São-Jorge", "nome_cientifico": "Dracaena trifasciata", "instrucoes_de_cuidado": "Muito resistente. Regar apenas quando o solo estiver bem seco.", "frequencia_rega_dias": 15},
            {"nome_popular": "Samambaia", "nome_cientifico": "Nephrolepis exaltata", "instrucoes_de_cuidado": "Gosta de muita umidade. Borrife água nas folhas.", "frequencia_rega_dias": 3},
        ]
        for especie_data in especies_iniciais:
            # Verifica se a espécie já existe antes de adicionar
            result = await db.execute(select(models.Especie).filter_by(nome_popular=especie_data["nome_popular"]))
            if not result.scalars().first():
                db_especie = models.Especie(**especie_data)
                db.add(db_especie)
        await db.commit()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    await popular_banco()
    yield

app = FastAPI(
    title="Jardineiro Digital API",
    description="Uma API para ajudar a cuidar das suas plantas.",
    version="1.0.0",
    lifespan=lifespan
)

# Endpoints para Jardineiro
@app.post("/jardineiros/", response_model=schemas.Jardineiro, tags=["Jardineiros"])
async def criar_jardineiro(jardineiro: schemas.JardineiroCreate, db: AsyncSession = Depends(get_db)):
    db_jardineiro = await crud.get_jardineiro_by_email(db, email=jardineiro.email)
    if db_jardineiro:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    return await crud.create_jardineiro(db=db, jardineiro=jardineiro)

# Endpoints para Especies
@app.post("/especies/", response_model=schemas.Especie, tags=["Espécies"])
async def criar_especie(especie: schemas.EspecieCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_especie(db=db, especie=especie)

@app.get("/especies/", response_model=list[schemas.Especie], tags=["Espécies"])
async def ler_especies(db: AsyncSession = Depends(get_db)):
    return await crud.get_especies(db)

# Endpoints para Plantas Cadastradas
@app.post("/jardineiros/{jardineiro_id}/plantas/", response_model=schemas.PlantaCadastrada, tags=["Minhas Plantas"])
async def criar_planta_para_jardineiro(jardineiro_id: int, planta: schemas.PlantaCadastradaCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_planta_para_jardineiro(db=db, planta=planta, jardineiro_id=jardineiro_id)
    
@app.get("/jardineiros/{jardineiro_id}/plantas/", response_model=list[schemas.PlantaCadastrada], tags=["Minhas Plantas"])
async def ler_plantas_do_jardineiro(jardineiro_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_plantas_do_jardineiro(db=db, jardineiro_id=jardineiro_id)

# Endpoints para Tarefas
@app.post("/plantas/{planta_id}/tarefas/", response_model=schemas.TarefaDeCuidado, tags=["Tarefas de Cuidado"])
async def registrar_tarefa_de_cuidado(planta_id: int, tarefa: schemas.TarefaDeCuidadoCreate, db: AsyncSession = Depends(get_db)):
    return await crud.log_tarefa_cuidado(db=db, tarefa=tarefa, planta_id=planta_id)

# Endpoint especial da "Funcionalidade UAU"
@app.get("/plantas/{planta_id}/proxima_rega/", response_model=schemas.ProximaRega, tags=["Lógica Inteligente"])
async def calcular_proxima_rega(planta_id: int, db: AsyncSession = Depends(get_db)):
    planta = await crud.get_planta_by_id(db, planta_id=planta_id)
    if not planta:
        raise HTTPException(status_code=404, detail="Planta não encontrada.")
    
    ultima_rega = await crud.get_ultima_rega(db, planta_id=planta_id)
    if not ultima_rega:
        return {"proxima_rega_em": None, "mensagem": "Esta planta nunca foi regada. Que tal regar agora?"}
        
    frequencia = planta.especie.frequencia_rega_dias
    proxima_data = ultima_rega.data_execucao.date() + datetime.timedelta(days=frequencia)
    
    return {"proxima_rega_em": proxima_data, "mensagem": f"Baseado na última rega, a próxima será em {proxima_data.strftime('%d/%m/%Y')}."}
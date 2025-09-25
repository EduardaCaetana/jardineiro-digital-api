# app/crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from . import models, schemas
import datetime

# CRUD para Jardineiro
async def create_jardineiro(db: AsyncSession, jardineiro: schemas.JardineiroCreate):
    db_jardineiro = models.Jardineiro(**jardineiro.model_dump())
    db.add(db_jardineiro)
    await db.commit()
    await db.refresh(db_jardineiro)
    return db_jardineiro

async def get_jardineiro_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.Jardineiro).filter(models.Jardineiro.email == email))
    return result.scalars().first()

# CRUD para Especie
async def create_especie(db: AsyncSession, especie: schemas.EspecieCreate):
    db_especie = models.Especie(**especie.model_dump())
    db.add(db_especie)
    await db.commit()
    await db.refresh(db_especie)
    return db_especie
    
async def get_especies(db: AsyncSession):
    result = await db.execute(select(models.Especie))
    return result.scalars().all()

# CRUD para PlantaCadastrada
async def create_planta_para_jardineiro(db: AsyncSession, planta: schemas.PlantaCadastradaCreate, jardineiro_id: int):
    db_planta = models.PlantaCadastrada(**planta.model_dump(), dono_id=jardineiro_id)
    db.add(db_planta)
    await db.commit()
    await db.refresh(db_planta)
    return db_planta
    
async def get_plantas_do_jardineiro(db: AsyncSession, jardineiro_id: int):
    result = await db.execute(
        select(models.PlantaCadastrada)
        .options(selectinload(models.PlantaCadastrada.especie))
        .filter(models.PlantaCadastrada.dono_id == jardineiro_id)
    )
    return result.scalars().all()
    
async def get_planta_by_id(db: AsyncSession, planta_id: int):
    result = await db.execute(
        select(models.PlantaCadastrada)
        .options(selectinload(models.PlantaCadastrada.especie))
        .filter(models.PlantaCadastrada.id == planta_id)
    )
    return result.scalars().first()

# CRUD para TarefaDeCuidado
async def log_tarefa_cuidado(db: AsyncSession, tarefa: schemas.TarefaDeCuidadoCreate, planta_id: int):
    db_tarefa = models.TarefaDeCuidado(**tarefa.model_dump(), planta_id=planta_id)
    db.add(db_tarefa)
    await db.commit()
    await db.refresh(db_tarefa)
    return db_tarefa
    
async def get_ultima_rega(db: AsyncSession, planta_id: int):
    result = await db.execute(
        select(models.TarefaDeCuidado)
        .filter_by(planta_id=planta_id, tipo_tarefa="Rega")
        .order_by(models.TarefaDeCuidado.data_execucao.desc())
    )
    return result.scalars().first()
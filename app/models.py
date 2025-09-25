# app/models.py
import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base

class Jardineiro(Base):
    __tablename__ = "jardineiros"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    plantas = relationship("PlantaCadastrada", back_populates="dono")

class Especie(Base):
    __tablename__ = "especies"
    id = Column(Integer, primary_key=True, index=True)
    nome_popular = Column(String, unique=True, index=True)
    nome_cientifico = Column(String, unique=True, index=True)
    instrucoes_de_cuidado = Column(Text)
    frequencia_rega_dias = Column(Integer)
    plantas_cadastradas = relationship("PlantaCadastrada", back_populates="especie")

class PlantaCadastrada(Base):
    __tablename__ = "plantas_cadastradas"
    id = Column(Integer, primary_key=True, index=True)
    apelido = Column(String, index=True)
    localizacao = Column(String)
    data_aquisicao = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    dono_id = Column(Integer, ForeignKey("jardineiros.id"))
    especie_id = Column(Integer, ForeignKey("especies.id"))
    dono = relationship("Jardineiro", back_populates="plantas")
    especie = relationship("Especie", back_populates="plantas_cadastradas")
    tarefas = relationship("TarefaDeCuidado", back_populates="planta", cascade="all, delete-orphan")

class TarefaDeCuidado(Base):
    __tablename__ = "tarefas_de_cuidado"
    id = Column(Integer, primary_key=True, index=True)
    tipo_tarefa = Column(String, index=True) # Ex: "Rega", "Adubação"
    data_execucao = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    planta_id = Column(Integer, ForeignKey("plantas_cadastradas.id"))
    planta = relationship("PlantaCadastrada", back_populates="tarefas")
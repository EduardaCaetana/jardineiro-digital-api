# app/schemas.py
from pydantic import BaseModel, ConfigDict
import datetime
from typing import Optional

# Schemas para TarefaDeCuidado
class TarefaDeCuidadoBase(BaseModel):
    tipo_tarefa: str

class TarefaDeCuidadoCreate(TarefaDeCuidadoBase):
    pass

class TarefaDeCuidado(TarefaDeCuidadoBase):
    id: int
    data_execucao: datetime.datetime
    model_config = ConfigDict(from_attributes=True)

# Schemas para Especie
class EspecieBase(BaseModel):
    nome_popular: str
    nome_cientifico: str
    instrucoes_de_cuidado: str
    frequencia_rega_dias: int

class EspecieCreate(EspecieBase):
    pass

class Especie(EspecieBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# Schemas para PlantaCadastrada
class PlantaCadastradaBase(BaseModel):
    apelido: str
    localizacao: str
    especie_id: int

class PlantaCadastradaCreate(PlantaCadastradaBase):
    pass

class PlantaCadastrada(PlantaCadastradaBase):
    id: int
    data_aquisicao: datetime.datetime
    especie: Especie
    tarefas: list[TarefaDeCuidado] = []
    model_config = ConfigDict(from_attributes=True)
    
class ProximaRega(BaseModel):
    proxima_rega_em: Optional[datetime.date] = None
    mensagem: str


# Schemas para Jardineiro
class JardineiroBase(BaseModel):
    nome: str
    email: str

class JardineiroCreate(JardineiroBase):
    pass

class Jardineiro(JardineiroBase):
    id: int
    plantas: list[PlantaCadastrada] = []
    model_config = ConfigDict(from_attributes=True)
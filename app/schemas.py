from pydantic import BaseModel, ConfigDict
from typing import Optional

class PlantaBase(BaseModel):
    nome_popular: str
    nome_cientifico: str
    familia: str
    origem: str
    cuidados: str

# ... (o resto do arquivo fica igual)

class PlantaCreate(PlantaBase):
    pass

class PlantaUpdate(PlantaBase):
    pass

class Planta(PlantaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
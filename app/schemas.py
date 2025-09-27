from pydantic import BaseModel, ConfigDict

class PlantaBase(BaseModel):
    nome_popular: str
    nome_cientifico: str
    familia: str
    origem: str
    cuidados: str

class PlantaCreate(PlantaBase):
    pass

class PlantaUpdate(PlantaBase):
    pass

class Planta(PlantaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
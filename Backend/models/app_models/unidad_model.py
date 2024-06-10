from pydantic import BaseModel


class Unidad(BaseModel):
    cod_unidad: int
    desc_unidad: str

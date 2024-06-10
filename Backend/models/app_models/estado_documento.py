from pydantic import BaseModel


class EstadoDocumento(BaseModel):
    cod_estado_documento: int
    desc_estado_documento: str

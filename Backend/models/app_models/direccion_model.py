from pydantic import BaseModel


class DireccionUsuario(BaseModel):
    cod_direccion_usuario: int
    desc_direccion_usuario: str
    cod_usuario: int
    cod_comuna: str
    cod_activa: str


class DireccionUsuarioCreate(BaseModel):
    desc_direccion_usuario: str
    cod_comuna: str


class DireccionCod(BaseModel):
    cod_direccion_usuario: int

from pydantic import BaseModel


class PersonalCreate(BaseModel):
    desc_personal: str
    login_personal: str
    contrasena: str
    cod_tipo_personal: int


class PersonalUpdate(BaseModel):
    cod_personal: int
    desc_personal: str
    login_personal: str
    contrasena: str
    cod_tipo_personal: int


class PersonalCod(BaseModel):
    cod_personal:  int

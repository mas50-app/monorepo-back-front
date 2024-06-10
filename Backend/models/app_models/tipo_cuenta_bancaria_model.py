from pydantic import BaseModel


class Tipo_cuenta_bancariaGet(BaseModel):
    cod_tipo_cuenta_bancaria: int
    desc_tipo_cuenta_bancaria: str


class Tipo_cuenta_bancariaCreate(BaseModel):
    desc_tipo_cuenta_bancaria: str


class Tipo_cuenta_bancariaUpdate(BaseModel):
    cod_tipo_cuenta_bancaria: int
    desc_tipo_cuenta_bancaria: str


class Tipo_cuenta_bancariaCod(BaseModel):
    cod_tipo_cuenta_bancaria: int

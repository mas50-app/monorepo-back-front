from pydantic import BaseModel


class TipoPagoGet(BaseModel):
    cod_tipo_pago: int
    desc_tipo_pago: str


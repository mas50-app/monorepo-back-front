from pydantic import BaseModel


class TipoAntecedentePost(BaseModel):
    desc_tipo_antecedente: str

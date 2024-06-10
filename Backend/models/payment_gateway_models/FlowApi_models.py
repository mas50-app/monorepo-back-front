from pydantic import BaseModel


class FlowApi(BaseModel):
    api_key: str
    api_url: str
    api_secret: str


class FlowEstadosDevolucion(BaseModel):
    created: str = "Solicitud Creada"
    accepted: str = "Reembolso Aceptado"
    rejected: str = "Reembolso Rechazado"
    refunded: str = "Reembolso Reintegrado"
    canceled: str = "Reembolso Cancelado"

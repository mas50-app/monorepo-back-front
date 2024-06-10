from pydantic import BaseModel


class Login(BaseModel):
    uuid: str
    token: str


class VerificaMail(BaseModel):
    mail: str

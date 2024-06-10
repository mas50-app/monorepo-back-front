from typing import List
from fastapi import APIRouter, Response, Header
from psycopg2.extras import RealDictCursor
from starlette.status import *
from bd_con.conexion import PsqlConnection
from dev_tools.json_web_token import validar_token
from middlewares.verifica_ruta_token import VerificaRutaToken
from models.app_models.direccion_model import DireccionUsuario, DireccionUsuarioCreate, DireccionCod

router = APIRouter(
    route_class=VerificaRutaToken
)


@router.get('/all', response_model=List[DireccionUsuario])
async def get_all_direcciones(response: Response, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT * FROM direccion_usuario 
                join comuna c on direccion_usuario.cod_comuna = c.cod_comuna
                WHERE cod_usuario = %s and cod_activa = 'S'"""
    cursor.execute(
        query,
        (
            token_info.get("cod_usuario"),
        )
    )
    direcciones = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return direcciones


@router.post('/crear')
async def create_direccion(response: Response, direccion: DireccionUsuarioCreate, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """INSERT INTO direccion_usuario (desc_direccion_usuario, user_id, cod_usuario, cod_comuna) 
            VALUES (%s,%s,%s,%s) returning cod_direccion_usuario"""
    cursor.execute(
        query,
        (
            direccion.desc_direccion_usuario,
            token_info.get("desc_usuario"),
            token_info.get("cod_usuario"),
            direccion.cod_comuna
        )
    )

    direcc = cursor.fetchone()
    conn.close()
    response.status_code = HTTP_201_CREATED
    return {"mensaje": f"Dirección creada con cod: {direcc.get('cod_direccion_usuario')} exitosamente"}


@router.put('/desactivar')
async def desactivar_direccion(response: Response, direccion: DireccionCod, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """UPDATE direccion_usuario SET cod_activa = 'N', user_id = %s WHERE cod_direccion_usuario = %s"""
    cursor.execute(
        query,
        (
            token_info.get("desc_usuario"),
            direccion.cod_direccion_usuario
        )
    )
    conn.close()
    response.status_code = HTTP_200_OK
    return {"mensaje": f"Dirección desactivada con cod: {direccion.cod_direccion_usuario} exitosamente"}


@router.post("/por_cod")
async def get_direccion_por_cod(response: Response, direcc: DireccionCod):
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT * FROM direccion_usuario WHERE cod_direccion_usuario = %s"""
    cursor.execute(
        query,
        (
            direcc.cod_direccion_usuario,
        )
    )
    direccion = cursor.fetchone()
    conn.close()
    response.status_code = HTTP_200_OK
    return direccion

from fastapi import APIRouter, Response, Header
from typing import List
from starlette.status import *
from bd_con.conexion import PsqlConnection
from psycopg2.extras import RealDictCursor

from dev_tools.json_web_token import validar_token
from middlewares.verifica_ruta_token import VerificaRutaToken
from models.app_models.tipo_cuenta_bancaria_model import Tipo_cuenta_bancariaGet, Tipo_cuenta_bancariaCreate, \
    Tipo_cuenta_bancariaUpdate, Tipo_cuenta_bancariaCod

router = APIRouter(route_class=VerificaRutaToken)


@router.get('/all', response_model=List[Tipo_cuenta_bancariaGet])
async def get_tipos_cuenta_bancaria(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT * FROM tipo_cuenta_bancaria"""
    cursor.execute(query)
    tipos_cuenta_bancaria = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return tipos_cuenta_bancaria


@router.post('/crear', response_model=None)
async def create_tipo_cuenta_bancaria(response: Response, tcb: Tipo_cuenta_bancariaCreate, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """INSERT INTO tipo_cuenta_bancaria (desc_tipo_cuenta_bancaria, user_id) 
                VALUES (%s, %s) returning cod_tipo_cuenta_bancaria"""
    cursor.execute(
        query,
        (
            tcb.desc_tipo_cuenta_bancaria,
            token_info.get("desc_personal")
        )
    )
    if cursor.fetchone():
        conn.close()
        response.status_code = HTTP_201_CREATED
        return 'Registro Creado'
    conn.close()
    response.status_code = HTTP_406_NOT_ACCEPTABLE
    return 'Registro no Creado'


@router.put('/actualizar', response_model=None)
async def update_tipo_cuenta_bancaria(response: Response, tcb: Tipo_cuenta_bancariaUpdate, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """UPDATE tipo_cuenta_bancaria SET 
                                desc_tipo_cuenta_bancaria = %s,
                                 user_id = %s 
                WHERE cod_tipo_cuenta_bancaria = %s"""
    cursor.execute(
        query,
        (
            tcb.desc_tipo_cuenta_bancaria,
            token_info.get("desc_personal"),
            tcb.cod_tipo_cuenta_bancaria
        )
    )
    conn.close()
    response.status_code = HTTP_200_OK
    return 'Registro actualizado exitosamente'


@router.delete('/borrar', response_model=None)
async def delete_tipo_cuenta_bancaria(response: Response, tcb: Tipo_cuenta_bancariaCod):
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """DELETE FROM tipo_cuenta_bancaria WHERE cod_tipo_cuenta_bancaria = %s"""
    try:
        cursor.execute(
            query,
            (
                tcb.cod_tipo_cuenta_bancaria,
            )
        )
        conn.close()
        response.status_code = HTTP_200_OK
        return "Registro eliminado exitosamente"
    except:
        conn.close()
        response.status_code = HTTP_409_CONFLICT
        return "No fue posible eliminar el registro"



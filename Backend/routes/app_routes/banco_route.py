from fastapi import APIRouter, Response
from starlette.status import *
from typing import List
from bd_con.conexion import PsqlConnection
from psycopg2.extras import RealDictCursor
from middlewares.verifica_ruta_token import VerificaRutaToken
from models.app_models.byCod_model import IndentifierCod
from models.app_models.banco_model import BancoCreate, BancoGet, BancoUpdate, BancoDelete
from models.app_models.tipo_cuenta_bancaria_model import Tipo_cuenta_bancariaGet

router = APIRouter(route_class=VerificaRutaToken)


@router.get('/all', response_model=List[BancoGet])
async def get_allbanco(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT * FROM banco ORDER BY cod_banco asc"""
    response.status_code = HTTP_200_OK
    cursor.execute(query)
    bancos = cursor.fetchall()
    conn.close()
    return bancos


@router.post('/por_cod', response_model=BancoGet)
async def get_by_cod_banco(response: Response, cod: IndentifierCod):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT * FROM banco WHERE cod_banco = %s"""
    cursor.execute(query, (cod.cod, ))
    banco = cursor.fetchone()
    return banco


@router.post('/crear', response_model=None)
async def create_banco(response: Response, banco: BancoCreate):
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """INSERT INTO banco (desc_banco) values (%s) returning cod_banco"""
    cursor.execute(query, (banco.desc_banco, ))
    cod_banco = cursor.fetchone().get('cod_banco')
    conn.close()
    response.status_code = HTTP_201_CREATED
    return {"mensaje": f"banco con cod: {cod_banco} creado exitosamente"}


@router.put('/actualizar')
async def update_banco(response: Response, banco: BancoUpdate):
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """UPDATE banco SET desc_banco = %s WHERE cod_banco = %s"""
    cursor.execute(query, (banco.desc_banco, banco.cod_banco, ))
    response.status_code = HTTP_200_OK
    conn.close()
    return {"mensaje": f"banco con cod: {banco.cod_banco} actualizado exitosamente"}


@router.delete('/eliminar', response_model=None)
async def delete_banco(response: Response, banco: BancoDelete):
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """DELETE FROM banco WHERE cod_banco = %s"""
    try:
        cursor.execute(query, (banco.cod_banco, ))
        conn.close()
        response.status_code = HTTP_200_OK
        return {"mensaje": f"Banco eliminado exitosamente"}
    except:
        conn.close()
        response.status_code = HTTP_409_CONFLICT
        return {"mensaje": f"Banco no se puede eliinar"}


@router.get('/tipos_cuenta_bancaria/all', response_model=List[Tipo_cuenta_bancariaGet])
async def delete_banco(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT * FROM tipo_cuenta_bancaria"""
    cursor.execute(query)
    tipos_cuenta_bancaria = cursor.fetchall()
    conn.close()
    return tipos_cuenta_bancaria



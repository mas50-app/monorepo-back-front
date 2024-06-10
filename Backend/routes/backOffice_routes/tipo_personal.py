from typing import List
from fastapi import APIRouter, Response, Header
from psycopg2.extras import RealDictCursor
from starlette.status import *
from bd_con.conexion import PsqlConnection
from dev_tools.json_web_token import validar_token
from middlewares.verifica_ruta_token import VerificaRutaToken
from models.backOffice_models.auth_model import TipoPersonal, PermisosPersonal, Permiso, PermisoCod, \
    CreateTipoPersonal, TipoPCod

router = APIRouter(route_class=VerificaRutaToken)


@router.get("/all", response_model=List[PermisosPersonal])
async def get_tipos_personal(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT 
                tp.*,
                 coalesce(json_agg(
                          (
                                 SELECT per
                                 FROM   (SELECT ptp.cod_permiso, p.desc_permiso) per)) filter (WHERE ptp.cod_permiso IS NOT NULL),'[]') permisos 
                FROM tipo_personal tp
                LEFT JOIN permiso_tipo_personal ptp on tp.cod_tipo_personal = ptp.cod_tipo_personal
                LEFT JOIN permiso p on ptp.cod_permiso = p.cod_permiso
                GROUP BY tp.cod_tipo_personal
                ORDER BY tp.cod_tipo_personal"""

    cursor.execute(
        query
    )
    tipos_personal = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return tipos_personal


@router.get("/permisos", response_model=List[Permiso])
async def get_permisos(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT p.cod_permiso, p.desc_permiso   
                FROM permiso p ORDER BY cod_permiso"""
    cursor.execute(
        query
    )
    permisos = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return permisos


@router.post("/create")
async def create_tipo_personal(response: Response, tp: CreateTipoPersonal, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """INSERT INTO tipo_personal (desc_tipo_personal, user_id) 
            VALUES (%s, %s) returning cod_tipo_personal"""
    cursor.execute(
        query,
        (
            tp.desc_tipo_personal,
            token_info.get("desc_personal")
        )
    )
    tipo_p = cursor.fetchone()
    conn.close()
    response.status_code = HTTP_201_CREATED
    return {"mensaje": f"Tipo Personal creado con cod: {tipo_p.get('cod_tipo_personal')} exitosamente"}


@router.put("/update")
async def update_tipo_personal(response: Response, tp: TipoPersonal, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """UPDATE tipo_personal SET desc_tipo_personal = %s, user_id = %s WHERE cod_tipo_personal = %s"""
    cursor.execute(
        query,
        (
            tp.desc_tipo_personal,
            token_info.get("desc_personal"),
            tp.cod_tipo_personal
        )
    )
    if tp.permisos:
        query = """DELETE FROM permiso_tipo_personal WHERE cod_tipo_personal = %s"""
        cursor.execute(
            query,
            (
                tp.cod_tipo_personal,
            )
        )
        query = """INSERT INTO permiso_tipo_personal (desc_permiso_tipo_personal, user_id, cod_tipo_personal, cod_permiso) 
                VALUES (%s,%s,%s,%s)"""
        for permiso in tp.permisos:
            cursor.execute(
                query,
                (
                    "",
                    token_info.get("desc_personal"),
                    tp.cod_tipo_personal,
                    permiso.cod_permiso
                )
            )
    conn.close()
    response.status_code = HTTP_200_OK
    return {"mensaje": f"Tipo Personal actualizado con cod: {tp.cod_tipo_personal} exitosamente"}


@router.delete("/delete")
async def delete_tipo_personal(response: Response, tp: TipoPCod):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """DELETE FROM permiso_tipo_personal WHERE cod_tipo_personal = %s"""
    cursor.execute(
        query,
        (
            tp.cod_tipo_personal,
        )
    )
    query = """DELETE FROM tipo_personal WHERE cod_tipo_personal = %s"""
    try:
        cursor.execute(
            query,
            (
                tp.cod_tipo_personal,
            )
        )
        conn.commit()
        conn.close()
        response.status_code = HTTP_200_OK
        return {"mensaje": f"Tipo Personal eliminado con cod: {tp.cod_tipo_personal} exitosamente"}
    except:
        conn.rollback()
        conn.close()
        response.status_code = HTTP_409_CONFLICT
        return {"mensaje": f"Tipo Personal tiene relaciones activas"}

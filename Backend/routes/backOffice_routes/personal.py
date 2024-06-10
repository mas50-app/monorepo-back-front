import hashlib
from typing import List
from fastapi import APIRouter, Response, Header
from psycopg2.extras import RealDictCursor
from starlette.status import *
from bd_con.conexion import PsqlConnection
from dev_tools.json_web_token import validar_token
from middlewares.verifica_ruta_token import VerificaRutaToken
from models.backOffice_models.personal_model import PersonalCreate, PersonalUpdate, PersonalCod

router = APIRouter(route_class=VerificaRutaToken)


@router.get("/all")
async def get_personal(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT    p.*,
                          tp.*,
                          coalesce(json_agg(
                          (
                                 SELECT per
                                 FROM   (
                                               SELECT ptp.cod_permiso ,
                                                      p2.desc_permiso) per)) filter (WHERE ptp.cod_permiso IS NOT NULL),'[]') permisos
                FROM      personal p
                join      tipo_personal tp
                USING    (cod_tipo_personal)
                left join permiso_tipo_personal ptp
                ON        tp.cod_tipo_personal = ptp.cod_tipo_personal
                left join permiso p2
                ON        ptp.cod_permiso = p2.cod_permiso
                GROUP BY  p.cod_personal,
                          tp.cod_tipo_personal
                ORDER BY p.cod_personal"""
    cursor.execute(query)
    personal = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return personal


@router.post("/create")
async def create_personal(response: Response, personal: PersonalCreate, Authorization: str = Header(None)):
    hash_pass = u"$MD5$%s" % (hashlib.md5(personal.contrasena.upper().encode()).hexdigest())
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """INSERT INTO personal (desc_personal, login_personal, contrasena, user_id, cod_tipo_personal) 
                VALUES (%s,%s,%s,%s,%s) returning cod_personal"""
    cursor.execute(
        query,
        (
            personal.desc_personal,
            personal.login_personal,
            hash_pass,
            token_info.get("desc_personal", ""),
            personal.cod_tipo_personal
        )
    )
    pers = cursor.fetchone()
    conn.close()
    if pers.get("cod_personal"):
        response.status_code = HTTP_201_CREATED
        return {"mensaje": f"Personal creado con cod: {pers.get('cod_personal')}"}
    response.status_code = HTTP_406_NOT_ACCEPTABLE
    return {"mensaje": "No se creó"}


@router.put("/update")
async def update_personal(response: Response, personal: PersonalUpdate, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    if personal.contrasena.find("$MD5$") != -1:
        query = """UPDATE personal SET 
                                    desc_personal = %s,
                                    login_personal = %s,
                                    user_id = %s,
                                    cod_tipo_personal = %s
                            WHERE cod_personal = %s"""
        cursor.execute(
            query,
            (
                personal.desc_personal,
                personal.login_personal,
                token_info.get("desc_personal", ""),
                personal.cod_tipo_personal,
                personal.cod_personal
            )
        )
    else:
        hash_pass = u"$MD5$%s" % (hashlib.md5(personal.contrasena.upper().encode()).hexdigest())
        query = """UPDATE personal SET 
                            desc_personal = %s,
                            login_personal = %s,
                            contrasena = %s,
                            user_id = %s,
                            cod_tipo_personal = %s
                    WHERE cod_personal = %s"""
        cursor.execute(
            query,
            (
                personal.desc_personal,
                personal.login_personal,
                hash_pass,
                token_info.get("desc_personal", ""),
                personal.cod_tipo_personal,
                personal.cod_personal
            )
        )
    conn.close()

    response.status_code = HTTP_201_CREATED
    return {"mensaje": f"Personal acualizado exitosamente"}


@router.delete("/delete")
async def delete_personal(response: Response, personal: PersonalCod, Authorization: str = Header(None)):
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """DELETE FROM personal WHERE cod_personal = %s"""
    try:
        cursor.execute(
            query,
            (
                personal.cod_personal,
            )
        )
        conn.close()
        response.status_code = HTTP_200_OK
        return {"mesnaje": f"Personal eliminado exitosamente"}
    except:
        conn.close()
        response.status_code = HTTP_409_CONFLICT
        return {"mensaje": f"No se pudo eliminar. Tiene relaciones"}

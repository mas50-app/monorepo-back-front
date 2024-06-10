from fastapi import APIRouter, Response, Header
from psycopg2.extras import RealDictCursor
from starlette.status import *
from bd_con.conexion import PsqlConnection
from dev_tools.json_web_token import validar_token
from middlewares.verifica_ruta_token import VerificaRutaToken
import hashlib

from models.backOffice_models.auth_model import RegistUser

router = APIRouter(route_class=VerificaRutaToken)


@router.post("/register")
async def personal_register(response: Response, personal: RegistUser, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    if token_info.get('cod_tipo_personal') != 1:
        response.status_code = HTTP_401_UNAUTHORIZED
        return {"mensaje": "tiene que ser administrador para poder registrar usuarios"}
    hash_pass = u"$MD5$%s" % (hashlib.md5(personal.contrasena.upper().encode()).hexdigest())
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
            token_info.get('desc_personal'),
            personal.cod_tipo_personal
        )
    )
    personal = cursor.fetchone()
    conn.close()
    if personal:
        response.status_code = HTTP_201_CREATED
        return {"mesaje": f"personal  con cod: {personal.get('cod_personal')} creado exitosamente"}
    response.status_code = HTTP_409_CONFLICT
    return {"mensaje": "no se creó el personal"}

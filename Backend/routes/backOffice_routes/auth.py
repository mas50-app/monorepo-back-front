from fastapi import APIRouter, Response, Header
from psycopg2.extras import RealDictCursor
from starlette.status import *
from bd_con.conexion import PsqlConnection
from dev_tools.json_web_token import generar_token, validar_token
from models.backOffice_models.auth_model import Login
import hashlib

router = APIRouter()


@router.post("/login")
async def login(response: Response, personal: Login):
    hash_pass = u"$MD5$%s" % (hashlib.md5(personal.contrasena.upper().encode()).hexdigest())
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT
                cod_personal,
                desc_personal,
                login_personal,
                tp.cod_tipo_personal, 
                tp.desc_tipo_personal
                FROM personal 
                JOIN tipo_personal tp on personal.cod_tipo_personal = tp.cod_tipo_personal
                WHERE login_personal = %s and contrasena = %s"""
    cursor.execute(
        query,
        (
            personal.login_personal,
            hash_pass
        )
    )
    personal = cursor.fetchone()
    conn.close()
    if not personal:
        response.status_code = HTTP_401_UNAUTHORIZED
        return {"mensaje": "personal no autorizado"}
    response.status_code = HTTP_200_OK
    return {"token": generar_token(personal)}


@router.get('/verifica-token')
def verificar_token(Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    # Retorna si es valido la info del token y si no un JsonResponse 401
    return token_info

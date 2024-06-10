from fastapi import APIRouter
from psycopg2.extras import RealDictCursor
from bd_con.conexion import PsqlConnection
from middlewares.verifica_ruta_token import VerificaRutaToken


router = APIRouter(
    route_class=VerificaRutaToken
)


@router.get("/all")
async def get_all_despachos():
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT * FROM despacho ORDER BY cod_despacho desc"""
    cursor.execute(query)
    despachos = cursor.fetchall()
    return despachos

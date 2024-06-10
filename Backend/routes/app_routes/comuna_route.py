from fastapi import APIRouter, Response
from starlette.status import *
from bd_con.conexion import PsqlConnection
from psycopg2.extras import RealDictCursor

router = APIRouter(
    # route_class=VerificaRutaToken
)


@router.get('/all',
            # response_model=List[CiudadGet]
            )
async def get_allciudad(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT r.cod_region,
                       r.desc_region,
                       Json_agg((SELECT d
                                 FROM   (SELECT cp.cod_provincia,
                                                cp.desc_provincia,
                                                cp.comunas)AS d)) AS provincias
                FROM   region r
                       JOIN (SELECT p.cod_provincia,
                                    p.desc_provincia,
                                    p.cod_region,
                                    Json_agg((SELECT x
                                              FROM   (SELECT c.cod_comuna,
                                                             c.desc_comuna)AS x)) AS comunas
                             FROM   provincia p
                                    JOIN comuna c using(cod_provincia)
                             GROUP  BY 1) AS cp
                         ON cp.cod_region = r.cod_region
                GROUP  BY 1, r.desc_region
                 ORDER BY 1"""
    cursor.execute(query)
    comunas = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return comunas

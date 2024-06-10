from fastapi import APIRouter, Response, Header
from starlette.status import *
from typing import List
from bd_con.conexion import PsqlConnection
from psycopg2.extras import RealDictCursor
from dev_tools.json_web_token import validar_token
from middlewares.verifica_ruta_token import VerificaRutaToken
from models.app_models.pago_model import PagoAllElement, FiltroMes

router = APIRouter(
    route_class=VerificaRutaToken
)


@router.post('/all', response_model=List[PagoAllElement])
async def get_pago_all(response: Response, mes: FiltroMes, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    cod_usuario = token_info.get('cod_usuario')
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    query = """SELECT 
                    pago.*,
                     d.*,
                     JSON_AGG((SELECT det 
                                FROM (select 
                                        dd.desc_detalle_documento,
                                        dd.cod_detalle_documento,
                                        dd.cantidad,
                                        dd.cod_item_servicio,
                                        s.desc_item_servicio,
                                        dd.subtotal
                                        ) as det)) as detalles
                FROM pago 
                JOIN documento d on pago.cod_documento = d.cod_documento
                JOIN detalle_documento dd on d.cod_documento = dd.cod_documento
                JOIN item_servicio s on dd.cod_item_servicio = s.cod_servicio
                WHERE d.cod_usuario_vendedor = %s and to_char(fecha_pago, 'YYYY-MM') = %s
                GROUP BY cod_pago, d.cod_documento, pago.fecha_pago, pago.hora_pago
                ORDER BY pago.fecha_pago desc, pago.hora_pago desc"""

    cursor.execute(
        query,
        (
            cod_usuario,
            mes.mes
        )
    )
    pagos = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return pagos


@router.post('/por_cod', response_model=None)
async def get_by_cod_pago(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    return 'Esta es la ruta GetByCod de pago'


@router.post('/actualizar', response_model=None)
async def update_pago(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    return 'Esta es la ruta Put o Update de pago'


@router.post('/borrar', response_model=None)
async def delete_pago(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    return 'Esta es la ruta Delete de pago'


@router.get('/filtro_meses', response_model=None)
async def get_meses_con_movimientos(response: Response, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    cod_usuario = token_info.get('cod_usuario')
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT 
                    DISTINCT ( To_char(p.fecha_pago, 'YYYY-MM') ) mes,
                    (array['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'])[to_char(p.fecha_pago,'mm')::int]||' '||to_char(p.fecha_pago,'yyyy') desc_mes
                FROM   pago p
                       JOIN documento d USING(cod_documento)
                WHERE  d.cod_usuario_vendedor = %s """
    cursor.execute(
        query,
        (
            cod_usuario,
        )
    )
    meses_con_movimientos = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return meses_con_movimientos

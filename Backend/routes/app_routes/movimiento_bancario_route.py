from fastapi import APIRouter, Response, Header
from starlette.status import *
from bd_con.conexion import PsqlConnection
from psycopg2.extras import RealDictCursor
from dev_tools.json_web_token import validar_token
from middlewares.verifica_ruta_token import VerificaRutaToken
from models.app_models.movimiento_bancario_model import FiltroMes, EstadoCuenta

router = APIRouter(
    # route_class=VerificaRutaToken
)


@router.get('/all', response_model=None)
async def get_allmovimiento_bancario(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    return 'Esta es la ruta GetAll de movimiento_bancario'


@router.post('/por_cod', response_model=None)
async def get_by_cod_movimiento_bancario(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    return 'Esta es la ruta GetByCod de movimiento_bancario'


@router.post('/crear', response_model=None)
async def create_movimiento_bancario(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    return 'Esta es la ruta Post o Create de movimiento_bancario'


@router.post('/actualizar', response_model=None)
async def update_movimiento_bancario(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    return 'Esta es la ruta Put o Update de movimiento_bancario'


@router.post('/borrar', response_model=None)
async def delete_movimiento_bancario(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    return 'Esta es la ruta Delete de movimiento_bancario'


@router.post('/estado_cuenta', response_model=EstadoCuenta)
async def get_estado_cuenta(response: Response, mes: FiltroMes,
                            # Authorization: str = Header(None)
                            ):
    # token = Authorization.split(" ")[1]
    # token_info = validar_token(token, output=True)
    # cod_usuario = token_info.get('cod_usuario')
    cod_usuario = 50
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    # datos_financieros = calcular_comision(cod_usuario, )
    # TODO: Donde esta la funcion sql now() debería estar un dia (Falta información de la idea de negocio)
    query = """SELECT d.cod_usuario_vendedor,
                       coalesce(Avg(p.monto_pago),0) as promedio_diario,
                       coalesce(Avg(p3.monto_pago),0) as promedio_semanal,
                       coalesce(Avg(p2.monto_pago),0) as promedio_mensual
                FROM   documento d
                       left join pago p
                              ON d.cod_documento = p.cod_documento
                                 AND To_char(p.fecha_pago, 'YYYY-MM') =
                                     To_char(Now(), 'YYYY-MM')
                       left join pago p2
                              ON d.cod_documento = p2.cod_documento
                                 AND To_char(p2.fecha_pago, 'YYYY-MM') = %s
                       left join pago p3
                              ON d.cod_documento = p3.cod_documento
                                 AND Extract(week FROM p3.fecha_pago :: DATE) = Extract(
                                     week FROM now() :: DATE)
                                 AND To_char(p3.fecha_pago, 'YYYY-MM') = %s
                WHERE  d.cod_usuario_vendedor = %s
                GROUP  BY 1 """
    cursor.execute(
        query,
        (
            mes.mes,
            mes.mes,
            cod_usuario
        )
    )
    movimientos = cursor.fetchone()
    query = """SELECT cod_usuario_vendedor,
                       To_char(fecha_pago, 'YYYY-MM') mes,
                       SUM(monto_pago) monto_mensual
                FROM   pago p
                       join documento d USING(cod_documento)
                WHERE  d.cod_usuario_vendedor = %s
                       AND To_char(fecha_pago, 'YYYY') = To_char(%s :: DATE, 'YYYY')
                GROUP  BY 1, 2"""
    cursor.execute(
        query,
        (
            cod_usuario,
            mes.mes+'-01'
        )
    )
    # Aqui se agrega un array de objetos con los meses y montos del año para el gráfico de Estado de Cuenta
    meses = [{"mes": str(i), "monto": 0} if i > 9 else {"mes": "0"+str(i), "monto": 0} for i in range(1, 13)]
    resumen_anual = cursor.fetchall()
    for mes in meses:
        for r in resumen_anual:
            if mes.get('mes') == r.get('mes').split("-")[1]:
                mes["monto"] = r.get('monto_mensual')
    movimientos['resumen_anual'] = meses
    conn.close()
    response.status_code = HTTP_200_OK
    return movimientos

from datetime import datetime
from typing import List

from fastapi import APIRouter, Response
from psycopg2.extras import RealDictCursor
from starlette.status import HTTP_200_OK

from bd_con.conexion import PsqlConnection
from middlewares.verifica_ruta_token import VerificaRutaToken
from models.app_models.movimiento_bancario_model import FiltroMes, Filtros

router = APIRouter(route_class=VerificaRutaToken)


def set_filtros(filtros: Filtros, anual: bool = False) -> str:
    condiciones = []

    if filtros.cod_categoria:
        condiciones.append(f"cs.cod_categoria IN ({', '.join(str(cod) for cod in filtros.cod_categoria)})")

    if filtros.cod_region:
        regiones = ', '.join(f"'{region}'" for region in filtros.cod_region)
        condiciones.append(f"r.cod_region IN ({regiones})")

    if filtros.desde and not anual:
        condiciones.append(f"d.fecha_documento >= '{filtros.desde}'")

    if filtros.hasta and not anual:
        condiciones.append(f"d.fecha_documento <= '{filtros.hasta}'")

    where_clause = " AND ".join(condiciones)
    return f"WHERE {where_clause}" if where_clause else ""


@router.get("/filtros")
async def get_filtros(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT 
                DISTINCT ( To_char(d.fecha_documento, 'YYYY-MM') ) mes,
                (array['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'])[to_char(d.fecha_documento,'mm')::int]||' '||to_char(d.fecha_documento,'yyyy') desc_mes
                FROM   documento d
                WHERE d.cod_estado_documento not in (1,4)
                ORDER BY mes desc"""
    cursor.execute(query)
    meses = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return meses


@router.post("/operaciones")
async def get_operaciones(response: Response, filtros: Filtros):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT d.cod_estado_documento,
                       ed.desc_estado_documento as name,
                       Count(d.cod_documento) as value
                FROM   documento d
                       join detalle_documento dd on d.cod_documento = dd.cod_documento
                       join item_servicio its on dd.cod_item_servicio = its.cod_item_servicio
                       join servicio s on its.cod_servicio = s.cod_servicio
                       join categoria_servicio cs on s.cod_servicio = cs.cod_servicio
                       join categoria cat on cs.cod_categoria = cat.cod_categoria 
                       join estado_documento ed USING(cod_estado_documento)
                       join usuario u on d.cod_usuario_vendedor = u.cod_usuario
                       join comuna c on u.cod_comuna = c.cod_comuna
                       join provincia p on c.cod_provincia = p.cod_provincia
                       join region r on p.cod_region = r.cod_region
                %s
                GROUP  BY d.cod_estado_documento,
                          ed.desc_estado_documento """ % (set_filtros(filtros))
    cursor.execute(
        query
    )
    operaciones = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return operaciones


@router.post("/ventas")
async def get_operaciones(response: Response, filtros: Filtros):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT ed.desc_estado_documento AS name,
                       Count(pa.cod_pago)        AS value
                FROM   pago pa
                       join documento d USING(cod_documento)
                       join detalle_documento dd on d.cod_documento = dd.cod_documento
                       join item_servicio its on dd.cod_item_servicio = its.cod_item_servicio
                       join servicio s on its.cod_servicio = s.cod_servicio
                       join categoria_servicio cs on s.cod_servicio = cs.cod_servicio
                       join categoria cat on cs.cod_categoria = cat.cod_categoria 
                       join estado_documento ed USING(cod_estado_documento)
                       join usuario u on d.cod_usuario_vendedor = u.cod_usuario
                       join comuna c on u.cod_comuna = c.cod_comuna
                       join provincia p on c.cod_provincia = p.cod_provincia
                       join region r on p.cod_region = r.cod_region
                %s
                GROUP  BY ed.desc_estado_documento """ % (set_filtros(filtros))
    cursor.execute(
        query
    )
    ventas = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return ventas


@router.post("/prestadores")
async def get_top_prestadores(response: Response, filtros: Filtros):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    # Prestadores con ventas aceptados o estados siguientes y no rechazadas
    query = """SELECT u.cod_usuario,
                       u.desc_usuario,
                       u.nombre_usuario as name,
                       coalesce(u.desc_talento_usuario, '') as desc_talento_usuario,
                       Count(d.cod_documento) AS value
                FROM   usuario u
                       JOIN documento d
                         ON d.cod_usuario_vendedor = u.cod_usuario
                            AND d.cod_estado_documento >= 2
                            AND d.cod_estado_documento != 4
                       join detalle_documento dd on d.cod_documento = dd.cod_documento
                       join item_servicio its on dd.cod_item_servicio = its.cod_item_servicio
                       join servicio s on its.cod_servicio = s.cod_servicio
                       join categoria_servicio cs on s.cod_servicio = cs.cod_servicio
                       join categoria cat on cs.cod_categoria = cat.cod_categoria 
                       join estado_documento ed USING(cod_estado_documento)
                       join comuna c on u.cod_comuna = c.cod_comuna
                       join provincia p on c.cod_provincia = p.cod_provincia
                       join region r on p.cod_region = r.cod_region 
                %s
                GROUP  BY u.cod_usuario
                LIMIT  5 """ % (set_filtros(filtros))
    cursor.execute(
        query
    )
    prestadores = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return prestadores


@router.post("/clientes")
async def get_top_clientes(response: Response, filtros: Filtros):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    # Clientes con compras aceptados o estados siguientes y no rechazadas
    query = """SELECT u.cod_usuario,
                       u.desc_usuario,
                       u.nombre_usuario as name,
                       coalesce(u.desc_talento_usuario, '') as desc_talento_usuario,
                       Count(d.cod_documento) AS value
                FROM   usuario u
                       JOIN documento d
                         ON d.cod_usuario_comprador = u.cod_usuario
                            AND d.cod_estado_documento >= 2
                            AND d.cod_estado_documento != 4
                       join detalle_documento dd on d.cod_documento = dd.cod_documento
                       join item_servicio its on dd.cod_item_servicio = its.cod_item_servicio
                       join servicio s on its.cod_servicio = s.cod_servicio
                       join categoria_servicio cs on s.cod_servicio = cs.cod_servicio
                       join categoria cat on cs.cod_categoria = cat.cod_categoria 
                       join estado_documento ed USING(cod_estado_documento)
                       join comuna c on u.cod_comuna = c.cod_comuna
                       join provincia p on c.cod_provincia = p.cod_provincia
                       join region r on p.cod_region = r.cod_region  
                %s
                GROUP  BY u.cod_usuario
                LIMIT  5 """ % (set_filtros(filtros))
    cursor.execute(
        query
    )
    clientes = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return clientes


@router.post("/ventas_mensual")
async def get_ventas_mensuales(response: Response, filtros: Filtros):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT to_char(fecha_documento, 'YYYY-MM-DD') as fecha_documento
                FROM generate_series(%s::DATE,date_trunc('month', %s::DATE) 
                        + interval '1 month' - interval '1 day', '1 days') as fecha_documento """
    cursor.execute(
        query,
        (
            filtros.desde.strftime("%Y-%m") + '-01' if filtros.desde else filtros.hasta.strftime("%Y-%m") + '-01',
            filtros.hasta.strftime("%Y-%m") + '-01'
        )
    )
    serie_fecha = cursor.fetchall()
    query = f"""SELECT to_char(d.fecha_documento, 'YYYY-MM-DD') as fecha_documento, SUM(Coalesce(d.monto_documento, 0)) AS monto
                FROM documento d
                left join detalle_documento dd on d.cod_documento = dd.cod_documento
               left join item_servicio its on dd.cod_item_servicio = its.cod_item_servicio
               left join servicio s on its.cod_servicio = s.cod_servicio
               left join categoria_servicio cs on s.cod_servicio = cs.cod_servicio
               left join categoria cat on cs.cod_categoria = cat.cod_categoria 
               left join estado_documento ed USING(cod_estado_documento)
               left join usuario u on d.cod_usuario_vendedor = u.cod_usuario
               left join comuna c on u.cod_comuna = c.cod_comuna
               left join provincia p on c.cod_provincia = p.cod_provincia
               left join region r on p.cod_region = r.cod_region
               where d.cod_estado_documento >= 2 AND d.cod_estado_documento != 4 AND d.fecha_documento in {tuple([s.get("fecha_documento") for s in serie_fecha])}
               {set_filtros(filtros, True).replace("WHERE", "AND")}
                GROUP BY d.fecha_documento
                ORDER BY d.fecha_documento ASC"""

    cursor.execute(query)
    ventas_x_mes = cursor.fetchall()
    result = []
    for mes in serie_fecha:
        result.append(
            {
                "name": mes.get("fecha_documento"),
                "value": [d.get("monto") for d in ventas_x_mes if mes.get("fecha_documento") == d.get("fecha_documento")][0] if [d.get("monto") for d in ventas_x_mes if mes.get("fecha_documento") == d.get("fecha_documento")] else 0
            }
        )
    conn.close()
    response.status_code = HTTP_200_OK
    return result


@router.post("/ventas_anual")
async def get_ventas_anual(response: Response, filtros: Filtros):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT to_char(generate_series(%s::DATE, %s::DATE, '1 month'), 'YYYY-MM') AS fecha_documento"""
    cursor.execute(
        query,
        (
            filtros.hasta.year.__str__() + '-01-01',
            filtros.hasta.year.__str__() + '-12-31'
        )
    )
    serie_meses = cursor.fetchall()
    query = f"""SELECT to_char(d.fecha_documento, 'YYYY-MM') as fecha_document, SUM(Coalesce(d.monto_documento, 0)) AS monto
                    FROM documento d
                    left join detalle_documento dd on d.cod_documento = dd.cod_documento
                   left join item_servicio its on dd.cod_item_servicio = its.cod_item_servicio
                   left join servicio s on its.cod_servicio = s.cod_servicio
                   left join categoria_servicio cs on s.cod_servicio = cs.cod_servicio
                   left join categoria cat on cs.cod_categoria = cat.cod_categoria 
                   left join estado_documento ed USING(cod_estado_documento)
                   left join usuario u on d.cod_usuario_vendedor = u.cod_usuario
                   left join comuna c on u.cod_comuna = c.cod_comuna
                   left join provincia p on c.cod_provincia = p.cod_provincia
                   left join region r on p.cod_region = r.cod_region
                   where d.cod_estado_documento >= 2 AND d.cod_estado_documento != 4 AND to_char(d.fecha_documento, 'YYYY-MM') in {tuple([s.get("fecha_documento") for s in serie_meses])}
                   {set_filtros(filtros, True).replace("WHERE", "AND")}
                    GROUP BY fecha_document
                    ORDER BY fecha_document ASC"""

    cursor.execute(query)
    ventas_x_anio = cursor.fetchall()
    result = []
    for mes in serie_meses:
        result.append(
            {
                "name": mes.get("fecha_documento"),
                "value":
                    [d.get("monto") for d in ventas_x_anio if mes.get("fecha_documento") == d.get("fecha_document")][
                        0] if [d.get("monto") for d in ventas_x_anio if
                               mes.get("fecha_documento") == d.get("fecha_document")] else 0
            }
        )
    conn.close()
    response.status_code = HTTP_200_OK
    return result


@router.post("/resumen_montos")
async def get_resumen_montos(response: Response, filtros: Filtros):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT SUM(monto_comision_bruto) - (SUM(monto_documento) * 0.0333) as utilidad_bruta,
                       SUM(monto_documento) * 0.0333 as flow_bruto,
                       SUM(monto_venta)         pagos_prestadores,
                       SUM(monto_iva)           iva_recaudado,
                       SUM(monto_documento) total_recaudado
                FROM   documento d
                        join detalle_documento dd on d.cod_documento = dd.cod_documento
                       join item_servicio its on dd.cod_item_servicio = its.cod_item_servicio
                       join servicio s on its.cod_servicio = s.cod_servicio
                       join categoria_servicio cs on s.cod_servicio = cs.cod_servicio
                       join categoria cat on cs.cod_categoria = cat.cod_categoria 
                       join estado_documento ed USING(cod_estado_documento)
                       join usuario u on d.cod_usuario_vendedor = u.cod_usuario
                       join comuna c on u.cod_comuna = c.cod_comuna
                       join provincia p on c.cod_provincia = p.cod_provincia
                       join region r on p.cod_region = r.cod_region
                        %s
                        cod_estado_documento NOT IN ( 1, 4 )
                       AND NOT EXISTS (SELECT cod_devolucion
                                       FROM   devolucion de
                                       WHERE  de.cod_documento = d.cod_documento) """ % (set_filtros(filtros) + "AND" if set_filtros(filtros) != "" else "WHERE ")
    cursor.execute(
        query
    )
    resumen = cursor.fetchone()
    conn.close()
    response.status_code = HTTP_200_OK
    return resumen if resumen.get("total_recaudado") else None

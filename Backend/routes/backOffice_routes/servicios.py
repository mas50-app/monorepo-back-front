from typing import List, Union
from fastapi import APIRouter, Response, Header
from psycopg2.extras import RealDictCursor
from starlette.status import *
from bd_con.conexion import PsqlConnection
from dev_tools.json_web_token import validar_token
from middlewares.verifica_ruta_token import VerificaRutaToken
from models.backOffice_models.servicios_model import Servicio, TopPrestacion, DetalleServicio, \
    ServicioCodUsuario, ServicioCod, DetalleVista, ItemServicioCod, UpdateDetalleVista, Filtros

router = APIRouter(
    route_class=VerificaRutaToken
)


def set_filtros(filtros: Filtros) -> str:
    condiciones = []

    if filtros.desde:
        condiciones.append(f"d.fecha_documento >= '{filtros.desde}'")

    if filtros.hasta:
        condiciones.append(f"d.fecha_documento <= '{filtros.hasta}'")

    where_clause = " AND ".join(condiciones)
    return f"AND {where_clause}" if where_clause else ""


@router.get("/all",
            response_model=Union[List[Servicio], None]
            )
async def get_all_prestaciones(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT s.*,
                      u.nombre_usuario,
                      u.desc_usuario,
                      coalesce(u.desc_talento_usuario, '') as desc_talento_usuario,
                      coalesce(json_agg((select com from (select sc.cod_comuna, c.desc_comuna) com)) FILTER (WHERE sc.cod_comuna IS NOT NULL),'[]') comunas,
                      coalesce(json_agg((select cat from (select cs.cod_categoria, ca.desc_categoria) cat)) FILTER (WHERE cs.cod_categoria IS NOT NULL),'[]') categorias
                FROM servicio s
                JOIN categoria_servicio cs on s.cod_servicio = cs.cod_servicio
                JOIN categoria ca on cs.cod_categoria = ca.cod_categoria
                LEFT JOIN servicio_comuna sc on s.cod_servicio = sc.cod_servicio
                LEFT JOIN comuna c on sc.cod_comuna = c.cod_comuna
                JOIN usuario u on s.cod_usuario = u.cod_usuario
                LEFT JOIN item_servicio ise on s.cod_servicio = ise.cod_servicio
                LEFT JOIN unidad u2 on ise.cod_unidad = u2.cod_unidad 
                group by s.cod_servicio, u.cod_usuario
                ORDER BY s.cod_servicio desc"""

    cursor.execute(
        query,
    )
    servicios = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return servicios


@router.post("/top_prestaciones", response_model=Union[List[TopPrestacion], None])
async def get_top_prestaciones(response: Response, filtros: Filtros):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT s.cod_servicio,
                       s.nom_servicio,
                       u.cod_usuario,
                       u.desc_usuario,
                       u.nombre_usuario,
                       Count(d.cod_documento) ventas
                FROM   servicio s
                       JOIN usuario u on u.cod_usuario = s.cod_usuario
                       LEFT JOIN item_servicio its using(cod_servicio)
                       LEFT JOIN detalle_documento dd USING(cod_item_servicio)
                       LEFT JOIN documento d
                              ON d.cod_documento = dd.cod_documento
                                 AND d.cod_estado_documento > 4 %s
                GROUP  BY s.cod_servicio, u.cod_usuario
                ORDER  BY ventas DESC
                LIMIT  %s """ % (set_filtros(filtros), filtros.cantidad)
    cursor.execute(query)
    top_prestaciones = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return top_prestaciones


@router.post("/por_cod",
             response_model=Union[DetalleServicio, None]
             )
async def get_servicio_detalle(response: Response, servicio: ServicioCodUsuario):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT    u.cod_usuario,
                          u.nombre_usuario,
                          u.apellido1_usuario,
                          u.apellido2_usuario,
                          u.desc_usuario,
                          u.rut_usuario,
                          u.mail_usuario,
                          u.comision,
                          u.path_imagen,
                          u.cod_activo,
                          coalesce(u.desc_talento_usuario, '') as desc_talento_usuario,
                          u.cod_comuna,
                          u.cod_revisado,
                          u.cod_pausado,
                          c.desc_comuna,
                          c.cod_provincia,
                          p.desc_provincia,
                          cb.cod_cuenta_bancaria,
                          cb.desc_cuenta_bancaria,
                          cb.cod_tipo_cuenta_bancaria,
                          cb.desc_tipo_cuenta_bancaria,
                          cb.nro_cuenta_bancaria,
                          cb.cod_banco,
                          cb.desc_banco,
                          Count(DISTINCT (e.cod_evaluacion)) valoraciones,
                          Avg(e.valor) valoracion_media,
                          COALESCE(
                              json_agg(
                                DISTINCT (
                                  SELECT ant
                                  FROM (
                                    SELECT a.*, ta.desc_tipo_antecedente
                                    WHERE a.cod_usuario = u.cod_usuario
                                  ) ant
                                  WHERE ant.cod_antecedente IS NOT NULL
                                )
                              ) FILTER (WHERE COALESCE((SELECT count(*) FROM antecedente WHERE cod_usuario = u.cod_usuario), 0) > 0),
                              '[]'
                            ) as docs                    
                FROM      usuario u
                join      comuna c
                USING     (cod_comuna)
                join      provincia p
                USING     (cod_provincia)
                left join      evaluacion e
                ON        e.cod_usuario_evaluado = u.cod_usuario
                left join antecedente a
                ON        a.cod_usuario = u.cod_usuario
                left join tipo_antecedente ta
                ON        a.cod_tipo_antecedente = ta.cod_tipo_antecedente
                left join
                          (
                                 SELECT cb1.*,
                                        tcb.desc_tipo_cuenta_bancaria,
                                        b.desc_banco
                                 FROM   cuenta_bancaria cb1
                                 join   tipo_cuenta_bancaria tcb
                                 USING  (cod_tipo_cuenta_bancaria)
                                 join   banco b
                                 USING  (cod_banco) ) AS cb
                ON        cb.cod_usuario = u.cod_usuario
                WHERE     u.cod_usuario = %s
                GROUP BY  u.cod_usuario,
                          cb.cod_cuenta_bancaria,
                          cb.desc_cuenta_bancaria,
                          cb.cod_tipo_cuenta_bancaria,
                          cb.desc_tipo_cuenta_bancaria,
                          cb.nro_cuenta_bancaria,
                          cb.cod_banco,
                          cb.desc_banco,
                          c.desc_comuna,
                          c.cod_provincia,
                          p.desc_provincia"""

    cursor.execute(
        query,
        (
            servicio.cod_usuario,
        )
    )
    serv = cursor.fetchone()
    # Agrupar los servicios correspondientes
    query = """SELECT 
                s.*, 
                coalesce(json_agg((select its from (select i.*, u.desc_unidad) its)) FILTER (WHERE i.cod_item_servicio IS NOT NULL),'[]') items
                FROM servicio s 
                LEFT JOIN item_servicio i on s.cod_servicio = i.cod_servicio
                LEFT JOIN unidad u on i.cod_unidad = u.cod_unidad
                WHERE s.cod_usuario = %s
                group by s.cod_servicio"""
    cursor.execute(
        query,
        (
            servicio.cod_usuario,
        )
    )
    serv['servicios'] = cursor.fetchall()
    # Agrupar los Courier del usuario
    query = """SELECT c.cod_courier, c.desc_courier, c.path_imagen FROM usuario_courier uc
                JOIN courier c on uc.cod_courier = c.cod_courier 
                WHERE cod_usuario = %s
                ORDER BY c.cod_courier"""
    cursor.execute(
        query,
        (
            servicio.cod_usuario,
        )
    )
    serv['couriers'] = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return serv


@router.get("/pendientes_revision")
async def get_servicios_revision_pendiente(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT
                s.cod_servicio, 
                desc_servicio, 
                cod_usuario, 
                direccion, 
                cod_retiro, 
                cod_domicilio, 
                cod_es_articulo, 
                nom_servicio, 
                desc_domicilio, 
                cod_activo, 
                cod_pausado, 
                dias_antelacion, 
                cod_revisado
                FROM servicio s WHERE cod_revisado = 'N'"""

    cursor.execute(query)
    servicios_prendientes = cursor.fetchall()
    response.status_code = HTTP_200_OK
    conn.close()
    return servicios_prendientes


@router.put("/cambio_estado_revisado")
async def set_revisado(response: Response, servicio: ServicioCod):
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """UPDATE servicio SET cod_revisado = 'S' WHERE cod_servicio = %s"""
    cursor.execute(
        query,
        (
            servicio.cod_servicio,
        )
    )
    response.status_code = HTTP_200_OK
    conn.close()
    return {"mensaje": f"Servicio con cod: {servicio.cod_servicio} cambiado a revisado exitosamente"}


@router.put("/cambio_estado_activo")
async def pivot_activo_inacitvo(response: Response, servicio: ServicioCod):
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """UPDATE servicio SET cod_activo = %s WHERE cod_servicio = %s"""
    cursor.execute(
        query,
        (
            servicio.enum_str,
            servicio.cod_servicio,
        )
    )
    response.status_code = HTTP_200_OK
    conn.close()
    return {"mensaje": f"Servicio con cod: {servicio.cod_servicio} cambiado exitosamente"}


@router.put("/cambio_estado_pausado")
async def pivot_pausado(response: Response, servicio: ServicioCod):
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """UPDATE servicio SET cod_pausado = %s WHERE cod_servicio = %s"""
    cursor.execute(
        query,
        (
            servicio.enum_str,
            servicio.cod_servicio,
        )
    )
    response.status_code = HTTP_200_OK
    conn.close()
    return {"mensaje": f"Servicio con cod: {servicio.cod_servicio} cambiado exitosamente"}


@router.put("/items/cambio_estado_activo")
async def pivot_item_activo(response: Response, item_serv: ItemServicioCod):
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """UPDATE item_servicio SET cod_activo = %s WHERE cod_item_servicio = %s"""
    cursor.execute(
        query,
        (
            item_serv.enum_str,
            item_serv.cod_item_servicio,
        )
    )
    response.status_code = HTTP_200_OK
    conn.close()
    return {"mensaje": f"Item con cod: {item_serv.cod_item_servicio} cambiado exitosamente"}


@router.post("/detalle", response_model=DetalleVista)
async def get_detalle_por_cod_serv(response: Response, servicio: ServicioCod):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT s.*,
                      u.nombre_usuario,
                      u.desc_usuario,
                      u.rut_usuario,
                      u.mail_usuario,
                      coalesce(u.desc_talento_usuario, '') as desc_talento_usuario,
                      coalesce (json_agg((select i from (select ise.*, u2.desc_unidad) i)) FILTER (WHERE ise.cod_item_servicio IS NOT NULL), '[]') items
                FROM servicio s 
                JOIN usuario u on s.cod_usuario = u.cod_usuario
                LEFT JOIN item_servicio ise using(cod_servicio)
                LEFT JOIN unidad u2 on ise.cod_unidad = u2.cod_unidad
                WHERE cod_servicio = %s
                group by s.cod_servicio, u.cod_usuario"""
    cursor.execute(
        query,
        (
            servicio.cod_servicio,
        )
    )
    serv = cursor.fetchone()
    query = """select u.*, e.* from evaluacion e
                join usuario u on e.cod_usuario_evaluador = u.cod_usuario 
                where e.cod_documento in (
                    select distinct(d.cod_documento) from documento d 
                    join detalle_documento dd using(cod_documento)
                    join item_servicio is2 on dd.cod_item_servicio = is2.cod_item_servicio
                    join servicio s using(cod_servicio)
                    where s.cod_servicio = %s
                )"""

    cursor.execute(
        query,
        (
            servicio.cod_servicio,
        )
    )
    evaluaciones = cursor.fetchall()
    valoracion_media = 0
    for ev in evaluaciones:
        valoracion_media += float(ev.get("valor"))
    valoracion_media = valoracion_media / evaluaciones.__len__() if evaluaciones else 0.0
    serv["valoraciones"] = {
        "valoracion_media": valoracion_media,
        # "evaluaciones": evaluaciones*20
        "evaluaciones": evaluaciones
    }
    # serv['items'] = serv.get("items")*20
    conn.close()
    response.status_code = HTTP_200_OK
    return serv


@router.put("/update")
async def update_servicio(response: Response, servicio: UpdateDetalleVista, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """UPDATE servicio SET 
                            user_id = %s,
                            desc_servicio = %s,
                            direccion = %s,
                            cod_retiro = %s,
                            cod_domicilio = %s,
                            cod_es_articulo = %s,
                            nom_servicio = %s,
                            desc_domicilio = %s,
                            dias_antelacion = %s,
                            cod_es_nacional= %s
                WHERE cod_servicio = %s"""
    cursor.execute(
        query,
        (
            token_info.get("desc_personal"),
            servicio.desc_servicio,
            servicio.direccion,
            servicio.cod_retiro,
            servicio.cod_domicilio,
            servicio.cod_es_articulo,
            servicio.nom_servicio,
            servicio.desc_domicilio,
            servicio.dias_antelacion,
            servicio.cod_es_nacional,
            servicio.cod_servicio
        )
    )
    query = """UPDATE usuario SET 
                                user_id = %s,
                                nombre_usuario = %s,
                                desc_usuario = %s,
                                rut_usuario = %s,
                                mail_usuario = %s
                WHERE cod_usuario = %s"""
    cursor.execute(
        query,
        (
            token_info.get("desc_personal"),
            servicio.nombre_usuario,
            servicio.desc_usuario,
            servicio.rut_usuario,
            servicio.mail_usuario,
            servicio.cod_usuario
        )
    )
    conn.close()
    response.status_code = HTTP_200_OK
    return {"mensaje": f"Registro actualizado exitosamente"}

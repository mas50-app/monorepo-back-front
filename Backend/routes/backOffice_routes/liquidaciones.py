import datetime
import os
from asyncio import sleep
from typing import List, Dict, Union
from fastapi import APIRouter, Response, Header, BackgroundTasks
from psycopg2.extras import RealDictCursor
from starlette.responses import FileResponse
from starlette.status import *

from bd_con.conexion import PsqlConnection
from dev_tools.json_web_token import validar_token
from dev_tools.pdf_generator import pdf_liquidacion
from middlewares.verifica_ruta_token import VerificaRutaToken
from models.backOffice_models.liquidaciones_model import UsuarioPendiente, UsuarioCod, LiquidacionCreate, \
    ResumenPorLiquidar, Liquidacion, LiquidAll, LiquidacionCod, LiquidacionPDF

router = APIRouter(
    route_class=VerificaRutaToken
)


@router.post("/all", response_model=LiquidAll)
async def get_all_liquidaciones(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = f"""SELECT l.*, u.* FROM liquidacion l
                JOIN usuario u on l.cod_usuario = u.cod_usuario"""
    cursor.execute(query)
    liquidaciones = cursor.fetchall()
    query = """SELECT count(l.cod_liquidacion) cant FROM liquidacion l"""
    cursor.execute(query)
    resp_data = {
        "length": cursor.fetchone().get("cant"),
        "liquidaciones": liquidaciones
    }
    conn.close()
    response.status_code = HTTP_200_OK
    return resp_data


@router.get("/usuarios_a_liquidar", response_model=List[UsuarioPendiente])
async def get_usuarios_con_liquidacion_pendiente(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT u.cod_usuario,
                        u.desc_usuario,
                        u.nombre_usuario,
                        u.apellido1_usuario,
                        u.rut_usuario,
                        u.mail_usuario,
                        u.comision,
                       Count(d.cod_documento) pendientes,
                       SUM(d.monto_documento) monto_total
                FROM   usuario u
                       join documento d
                         ON u.cod_usuario = d.cod_usuario_vendedor
                WHERE  NOT EXISTS (SELECT *
                                   FROM   detalle_liquidacion dl
                                   WHERE  dl.cod_documento = d.cod_documento)
                                   and d.cod_estado_documento >= 6
                GROUP  BY u.cod_usuario """
    cursor.execute(
        query
    )
    pendientes = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return pendientes


@router.post("/documentos_pendientes_por_usuario", response_model=Union[ResumenPorLiquidar, None])
async def get_documentos_pendiente_por_usuario(response: Response, usuario: UsuarioCod):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """ SELECT d.*,
                        monto_comision_neto,
                        monto_iva,
                        monto_comision_bruto,
                        monto_venta as monto_liquidacion,
                        ed.desc_estado_documento,
                        u.comision
                    FROM documento d
                    JOIN estado_documento ed USING(cod_estado_documento)
                    JOIN usuario u ON d.cod_usuario_comprador = u.cod_usuario
                    JOIN cuenta_bancaria cb on u.cod_usuario = cb.cod_usuario
                    JOIN tipo_cuenta_bancaria tc on cb.cod_tipo_cuenta_bancaria = tc.cod_tipo_cuenta_bancaria
                    JOIN banco b on cb.cod_banco = b.cod_banco
                    WHERE cod_usuario_vendedor = %s
                        AND d.cod_estado_documento >= 6
                        AND NOT EXISTS (
                            SELECT cod_detalle_liquidacion
                            FROM detalle_liquidacion dl
                            WHERE dl.cod_documento = d.cod_documento
                        )"""
    cursor.execute(
        query,
        (
            usuario.cod_usuario,
        )
    )
    docs = cursor.fetchall()
    query = """SELECT SUM(monto_documento) AS monto_total_ventas,
                       SUM(monto_comision_bruto) AS monto_total_comision,
                       SUM(monto_venta) AS monto_total_liquidacion
                FROM   documento d
                       join usuario u
                         ON d.cod_usuario_comprador = u.cod_usuario
                WHERE cod_usuario_vendedor = %s
                        AND d.cod_estado_documento >= 6
                        AND NOT EXISTS (
                            SELECT cod_detalle_liquidacion
                            FROM detalle_liquidacion dl
                            WHERE dl.cod_documento = d.cod_documento
                        )"""
    cursor.execute(
        query,
        (
            usuario.cod_usuario,
        )
    )
    resumen = cursor.fetchone()
    conn.close()
    resumen["docs"] = docs
    response.status_code = HTTP_200_OK
    return resumen


@router.post("/crear")
async def create_liquidacion(response: Response, liquidacion: LiquidacionCreate, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """INSERT INTO liquidacion (desc_liquidacion, user_id, fecha_liquidacion, monto_liquidacion, monto_venta, comision, cod_usuario) 
                VALUES (%s,%s,%s,%s,%s,%s,%s) returning cod_liquidacion"""
    cursor.execute(
        query,
        (
            liquidacion.desc_liquidacion,
            token_info.get("desc_personal"),
            datetime.datetime.today(),
            liquidacion.monto_liquidacion,
            liquidacion.monto_venta,
            liquidacion.comision,
            liquidacion.cod_usuario
        )
    )
    liquid = cursor.fetchone()
    for detalle in liquidacion.detalles:
        query = """INSERT INTO detalle_liquidacion (desc_detalle_liquidacion, cod_liquidacion, cod_documento, monto_documento) 
                    VALUES (%s,%s,%s,%s)"""
        cursor.execute(
            query,
            (
                detalle.desc_detalle_liquidacion,
                liquid.get("cod_liquidacion"),
                detalle.cod_documento,
                detalle.monto_documento
            )
        )
    query = """SELECT cod_cuenta_bancaria FROM cuenta_bancaria WHERE cod_usuario = %s"""
    cursor.execute(query,
                   (
                       liquidacion.cod_usuario,
                   ))
    cuenta_bancaria = cursor.fetchone()
    query = """INSERT INTO movimiento_bancario (desc_movimiento_bancario, user_id, cod_tipo_movimiento_bancario, monto, fecha, cod_cuenta, cod_liquidacion) 
            VALUES (%s,%s,%s,%s,%s,%s,%s)"""
    cursor.execute(
        query,
        (
            "",
            token_info.get("desc_personal", ""),
            1,
            liquidacion.monto_liquidacion,
            datetime.date.today(),
            cuenta_bancaria.get("cod_cuenta_bancaria"),
            liquid.get("cod_liquidacion")
        )
    )
    conn.close()
    response.status_code = HTTP_201_CREATED
    return {"mensaje": f"Liquidación creada exitosamente con cod: {liquid.get('cod_liquidacion')}"}


@router.post("/historico_por_prestador", response_model=List[Liquidacion])
async def get_historico_por_prestador(response: Response, prestador: UsuarioCod):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT l.cod_liquidacion, l.desc_liquidacion, 
                        l.monto_venta, l.monto_liquidacion, 
                        l.comision / l.monto_venta * 100 as comision,
                        to_char(l.fecha_liquidacion, 'DD-MM-YYYY') as fecha_liquidacion, 
                        l.comision as monto_comision,
                       Json_agg((SELECT det
                                 FROM   (SELECT dl.*,
                                                d.*) det)) AS detalles
                FROM   liquidacion l
                       JOIN detalle_liquidacion dl using(cod_liquidacion)
                       JOIN documento d
                         ON dl.cod_documento = d.cod_documento
                WHERE  l.cod_usuario = %s
                GROUP  BY l.cod_liquidacion"""

    cursor.execute(
        query,
        (
            prestador.cod_usuario,
        )
    )
    liquidaciones = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return liquidaciones


@router.post("/download-pdf")
async def download_pdf(response: Response, liquidacion: LiquidacionCod, background_tasks: BackgroundTasks):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT l.cod_liquidacion,
                       l.desc_liquidacion,
                       l.fecha_liquidacion,
                       l.monto_liquidacion,
                       l.monto_venta,
                       u.cod_usuario,
                       u.nombre_usuario,
                       u.rut_usuario,
                       u.mail_usuario,
                       u.cod_comuna,
                       c.desc_comuna,
                       Json_agg(dl) detalles
                FROM   liquidacion l
                       join detalle_liquidacion dl USING(cod_liquidacion)
                       join usuario u USING(cod_usuario)
                       join comuna c USING(cod_comuna)
                WHERE l.cod_liquidacion = %s
                GROUP  BY l.cod_liquidacion,
                          u.cod_usuario,
                          c.desc_comuna """
    cursor.execute(
        query,
        (
            liquidacion.cod_liquidacion,
        )
    )
    liquid = cursor.fetchone()
    conn.close()
    pdf_temp = pdf_liquidacion(LiquidacionPDF(**liquid))

    # Eliminar el archivo temporal después de enviar la respuesta
    async def eliminar_archivo_temporal():
        await sleep(1)
        os.remove(pdf_temp)
        print("------- PDF temporal removed -------")

    background_tasks.add_task(eliminar_archivo_temporal)
    response.status_code = HTTP_200_OK
    return FileResponse(pdf_temp)

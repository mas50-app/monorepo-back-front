import os
import uuid
from typing import List
from PIL import Image
from io import BytesIO
from fastapi import APIRouter, Response, UploadFile, File, Form, Header, Request
from starlette.status import *
from bd_con.conexion import PsqlConnection
from psycopg2.extras import RealDictCursor
from dev_tools.json_web_token import validar_token
from middlewares.verifica_ruta_token import VerificaRutaToken
from models.app_models.courier_model import CourierGet, CourierDelete, PrestadorCod, CourierAsociado, CourierAsociar
from models.backOffice_models.usuarios_model import UsuarioCod

router = APIRouter(
    route_class=VerificaRutaToken
)


@router.get('/all', response_model=List[CourierGet])
async def get_all_courier(response: Response):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT * FROM courier ORDER BY cod_courier"""
    cursor.execute(query)
    couriers = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return couriers


@router.post('/create')
async def create_courier(
        response: Response,
        img: UploadFile = File(None),
        desc_courier: str = Form(...),
        link_courier: str = Form(...),
        Authorization: str = Header(None)
):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)

    # Guardar Imagen (Logo)
    if img:
        img_uuid = uuid.uuid4()
        formato = "png"
        file = await img.read()
        image = Image.open(BytesIO(file))
        image = image.resize((image.width // 2, image.height // 2))
        if os.name == 'nt':
            image.save(os.path.join("temporales_desarrollo", "imagenes", f"{img_uuid}.{formato}"), "PNG")
        else:
            image.save("/" + os.path.join("app", "temporales_desarrollo", "imagenes", f"{img_uuid}.{formato}"), "PNG")
        path_imagen = f"{img_uuid}.{formato}"
    else:
        path_imagen = None
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """INSERT INTO courier (desc_courier, user_id, link_courier, path_imagen) 
                VALUES (%s,%s,%s,%s)"""
    cursor.execute(
        query,
        (
            desc_courier,
            token_info.get("desc_personal"),
            link_courier,
            path_imagen
        )
    )
    conn.close()
    response.status_code = HTTP_201_CREATED
    return {"mensaje": "Courier Creado Exitosamente"}


@router.put("/update")
async def update_courier(
        response: Response,
        img: UploadFile = File(None),
        cod_courier: int = Form(...),
        desc_courier: str = Form(...),
        link_courier: str = Form(...),
        Authorization: str = Header(None)
):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    if img:
        file = await img.read()
        query = """SELECT path_imagen FROM courier WHERE cod_courier = %s"""
        cursor.execute(
            query,
            (
                cod_courier,
            )
        )
        courier_image = cursor.fetchone()
        if not courier_image.get("path_imagen"):
            img_uuid = uuid.uuid4()
            formato = "png"
            image = Image.open(BytesIO(file))

            if os.name == 'nt':
                image.save(os.path.join("temporales_desarrollo", "imagenes", f"{img_uuid}.{formato}"), "PNG")
            else:
                image.save("/" + os.path.join("app", "temporales_desarrollo", "imagenes", f"{img_uuid}.{formato}"), "PNG")
            query = """UPDATE courier SET desc_courier = %s, user_id = %s, link_courier = %s, path_imagen = %s WHERE cod_courier = %s"""
            cursor.execute(
                query,
                (
                    desc_courier,
                    token_info.get("desc_personal"),
                    link_courier,
                    f"{img_uuid}.{formato}",
                    cod_courier
                )
            )
        else:
            path = courier_image.get("path_imagen")
            if os.name == 'nt':
                file_path = os.path.join("temporales_desarrollo", "imagenes")
            else:
                file_path = "/" + os.path.join("app", "temporales_desarrollo", "imagenes")

            # Elimino la imagen existente
            if os.path.exists(f"{file_path}{path}"):
                os.remove(f"{file_path}{path}")

            image = Image.open(BytesIO(file))
            image = image.resize((image.width // 2, image.height // 2))
            image.save(os.path.join(f"{file_path}", path), "PNG")
            query = """UPDATE courier SET desc_courier = %s, user_id = %s, link_courier = %s WHERE cod_courier = %s"""
            cursor.execute(
                query,
                (
                    desc_courier,
                    token_info.get("desc_personal"),
                    link_courier,
                    cod_courier
                )
            )
    conn.close()
    response.status_code = HTTP_200_OK
    return {"mensaje": "Courier Actualizado exitosamente"}


@router.delete("/delete")
async def delete_courier(response: Response, courier: CourierDelete):
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """DELETE FROM courier WHERE cod_courier = %s"""
    try:
        cursor.execute(
            query,
            (
                courier.cod_courier,
            )
        )
        conn.close()
        response.status_code = HTTP_200_OK
        return {"mensaje": "Courier eliminado exitosamente"}
    except:
        conn.close()
        response.status_code = HTTP_409_CONFLICT
        return {"mensaje": "Courier no se puede eliminar, tiene relaciones activas"}


@router.post('/por-cod-prestador', response_model=List[CourierAsociado])
async def get_couriers_by_prestador(response: Response, prestador: PrestadorCod):
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT * FROM usuario_courier 
                LEFT JOIN courier c on usuario_courier.cod_courier = c.cod_courier
                WHERE cod_usuario = %s"""
    cursor.execute(
        query,
        (
            prestador.cod_usuario,
        )
    )
    couriers = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return couriers


@router.put("/asociar-por-prestador")
async def set_courier_by_prestador(response: Response, courier: CourierAsociar, Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """DELETE FROM usuario_courier WHERE cod_usuario = %s"""
    cursor.execute(
        query,
        (
            courier.cod_usuario,
        )
    )
    query = """INSERT INTO usuario_courier (desc_usuario_courier, user_id, cod_usuario, cod_courier) 
                VALUES (%s,%s,%s,%s)"""

    for co in courier.couriers:
        cursor.execute(
            query,
            (
                "",
                token_info.get("desc_usuario") if token_info.get("desc_usuario") else token_info.get("desc_personal"),
                courier.cod_usuario,
                co.cod_courier
            )
        )

    conn.close()
    response.status_code = HTTP_200_OK
    return {"mensaje": f"Couriers asociado a prestador con cod:{courier.cod_usuario} exitosamente"}

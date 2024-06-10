from typing import List
from fastapi import APIRouter, Response, Header
from psycopg2.extras import RealDictCursor
from starlette.status import *
from bd_con.conexion import PsqlConnection
from dev_tools.json_web_token import validar_token
from middlewares.verifica_ruta_token import VerificaRutaToken
from models.app_models.item_model import Item, ItemCodServ, ItemCod

router = APIRouter(
    route_class=VerificaRutaToken
)


@router.post("/all", response_model=List[Item])
async def get_items_by_service(
        response: Response,
        item: ItemCodServ,
):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT it.*,
                       CASE
                         WHEN Count(dd.cod_detalle_documento) > 0 THEN FALSE
                         ELSE TRUE
                       END editable
                FROM   item_servicio it
                LEFT JOIN detalle_documento dd USING(cod_item_servicio)
                WHERE  it.cod_servicio = %s
                GROUP  BY it.cod_item_servicio"""

    cursor.execute(
        query,
        (
            item.cod_servicio,
        )
    )
    items = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    return items


@router.post("/create")
async def create_item(
        response: Response,
        item: Item,
        Authorization: str = Header(None)
):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """INSERT INTO item_servicio (desc_item_servicio, cod_servicio, cod_unidad, valor_unidad, user_id)
                VALUES (%s,%s,%s,%s,%s) returning cod_item_servicio"""
    cursor.execute(
        query,
        (
            item.desc_item_servicio,
            item.cod_servicio,
            item.cod_unidad,
            item.valor_unidad,
            token_info.get("desc_usuario")
        )
    )

    cod_item = cursor.fetchone().get('cod_item_servicio')

    conn.close()
    response.status_code = HTTP_201_CREATED
    return {"mensaje": f"item con cod {cod_item} creado exitosamente"}


@router.put("/update")
async def create_item(
        response: Response,
        item: Item,
        Authorization: str = Header(None)
):
    token = Authorization.split(" ")[1]
    token_info = validar_token(token, output=True)
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    item = item.dict(exclude_none=True)

    query = f"""UPDATE item_servicio set user_id = %s, 
                    {','.join([f'{u}={"%s"}' for u in item.keys() if u not in ['cod_item_servicio']])}"""
    query += " WHERE cod_item_servicio = %s"
    valores = [token_info.get('desc_usuario')]

    for i in item.keys():
        if i not in ['cod_item_servicio']:
            valores.append(item.get(i))

    valores.append(item.get('cod_item_servicio'))
    print(query, valores)
    cursor.execute(
        query,
        valores
    )

    conn.close()
    response.status_code = HTTP_200_OK
    return {"mensaje": f"item con cod: {item.get('cod_item_servicio')} actualizado exitosamente"}


# @router.post('/subir_imagen')
# async def subir_imagen_item(
#         response: Response,
#         file: UploadFile = File(),
#         cod_item_servicio: int = Form(...),
#         Authorization: str = Header(None)):
#     # x = await req.form()
#     token = Authorization.split(" ")[1]
#     token_info = validar_token(token, output=True)
#
#     conn = PsqlConnection().conn
#     conn.autocommit = True
#     cursor = conn.cursor(cursor_factory=RealDictCursor)
#
#     file_name = f'{cod_item_servicio}_{token_info.get("apellido1_usuario")}_{token_info.get("nombre_usuario")}_{file.filename}'
#     file = await file.read()
#     if os.name == 'nt':
#         file_path = f'./temporales_desarrollo/imagenes/items/{file_name}'
#     else:
#         file_path = f'.\\temporales_desarrollo\\imagenes\\items\\{file_name}'
#     with open(file_path, 'wb') as f:
#         f.write(file)
#         f.close()
#
#     query = """INSERT INTO imagen (desc_imagen, user_id, path_temporal, cod_item_servicio)
#             VALUES (%s,%s,%s,%s) returning cod_imagen"""
#
#     cursor.execute(
#         query,
#         (
#             " ",
#             token_info.get('desc_usuario'),
#             file_path,
#             cod_item_servicio
#         )
#     )
#
#     cod_imagen = cursor.fetchone().get('cod_imagen')
#     conn.close()
#     response.status_code = HTTP_201_CREATED
#     return {"mensaje": f"Imagen con cod {cod_imagen} guardada exitosamente"}


# @router.post("/get_imagen")
# async def get_imagen_by_cod(response: Response, imagen: ImagenByCod):
#     conn = PsqlConnection().conn
#     cursor = conn.cursor(cursor_factory=RealDictCursor)
#
#     query = """SELECT * FROM imagen WHERE cod_imagen = %s"""
#     cursor.execute(
#         query,
#         (
#             imagen.cod_imagen,
#         )
#     )
#
#     path = cursor.fetchone().get('path_temporal')
#     return FileResponse(path=path)


@router.post("/delete")
async def delete_or_inactivate_item(response: Response, item: ItemCod):
    """Solo si no hay relaciones ya efectuada con este item se elimina si no se inactiva"""
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    if item.editable:

        query = """DELETE FROM item_servicio WHERE cod_item_servicio = %s"""
        cursor.execute(
            query,
            (
                item.cod_item_servicio,
            )
        )

        conn.close()
        response.status_code = HTTP_200_OK
        return {"mensaje": f"Item con cod {item.cod_item_servicio} eliminado exitosamente"}

    else:
        query = """UPDATE item_servicio SET cod_activo = 'N' WHERE cod_item_servicio = %s"""
        cursor.execute(
            query,
            (
                item.cod_item_servicio,
            )
        )
        conn.close()
        response.status_code = HTTP_200_OK
        return {"mensaje": f"Item con cod {item.cod_item_servicio} desactivado exitosamente"}

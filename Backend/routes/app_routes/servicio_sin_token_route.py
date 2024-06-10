from fastapi import APIRouter, Response
from starlette.status import HTTP_200_OK
from unidecode import unidecode
from models.app_models.servicio_model import ServicioBuscador, RespPorCod, ServicioCod
from bd_con.conexion import PsqlConnection
from psycopg2.extras import RealDictCursor

router = APIRouter()


@router.post('/buscar', response_model=None)
async def buscar_servicio_st(response: Response, filtro: ServicioBuscador):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    print("FILTROS", filtro)
    if filtro.filtro == "":
        query = """SELECT u.cod_usuario,
                           u.desc_usuario,
                           u.nombre_usuario,
                           coalesce(u.desc_talento_usuario, '') as desc_talento_usuario,
                           s.cod_servicio,
                           s.desc_servicio,
                           s.nom_servicio,
                           s.dias_antelacion,
                           s.path_imagen,
                           false as favorito,
                           Coalesce(Avg(e.valor), 5.0)    AS valoracion,
                           json_agg(its.*) items,
                           coalesce(c2.cod_comuna, '') as cod_comuna
                    FROM   servicio s
                           JOIN usuario u on s.cod_usuario = u.cod_usuario and u.cod_eliminado = 'N' and u.cod_pausado = 'N' and u.cod_activo = 'S'
                           join item_servicio its using(cod_servicio)
                           LEFT JOIN servicio_comuna sc ON s.cod_servicio = sc.cod_servicio
                           LEFT JOIN comuna c2 ON sc.cod_comuna = c2.cod_comuna
                           LEFT JOIN evaluacion e ON e.cod_usuario_evaluado = s.cod_usuario
                           JOIN categoria_servicio cs ON cs.cod_servicio = s.cod_servicio
                           JOIN categoria c USING(cod_categoria)
                    WHERE  s.cod_pausado = 'N' AND s.cod_activo = 'S' AND (c2.cod_comuna = %s OR s.cod_es_nacional = 'S')
                    GROUP  BY 1,2,3,4,5,6,7,s.dias_antelacion, desc_usuario, c2.cod_comuna
                    ORDER  BY valoracion, desc_usuario
                    LIMIT  20"""

        cursor.execute(
            query,
            (
                filtro.cod_comuna,
            )
        )
        servicios = cursor.fetchall()
        conn.close()
        response.status_code = HTTP_200_OK
        print("SErvicios", servicios)
        return servicios

    query = """SELECT 
                        u.cod_usuario,
                       u.desc_usuario,
                       u.nombre_usuario,
                       coalesce(u.desc_talento_usuario, '') as desc_talento_usuario,
                       s.cod_servicio,
                       s.desc_servicio,
                       s.nom_servicio,
                       s.dias_antelacion,
                       s.path_imagen,
                       false as favorito,
                       coalesce (Avg(e.valor), 5.0) AS valoracion,
                       json_agg(its.*) items,
                       coalesce (c2.cod_comuna, '') as cod_comuna
                FROM   (WITH words AS (
                                        SELECT word
                                            FROM (
                                              SELECT unnest(string_to_array(%s, ' ')) AS word
                                            ) filtro_palabras
                                        WHERE word != 'y/o'
                                        )
                                        SELECT string_agg(word, ' | ') busqueda
                                        FROM words) filtro, servicio s
                       JOIN usuario u on s.cod_usuario = u.cod_usuario and u.cod_eliminado = 'N' and u.cod_pausado = 'N' and u.cod_activo = 'S'
                       join item_servicio its using(cod_servicio)
                       LEFT JOIN servicio_comuna sc
                             ON s.cod_servicio = sc.cod_servicio
                           LEFT JOIN comuna c2
                             ON sc.cod_comuna = c2.cod_comuna
                       left join evaluacion e
                         ON e.cod_usuario_evaluado = s.cod_usuario
                       join categoria_servicio cs on cs.cod_servicio = s.cod_servicio 
                       join categoria c USING(cod_categoria)
                WHERE (
                to_tsvector('spanish', u.desc_usuario) @@ to_tsquery('spanish', busqueda)  or similarity( u.desc_usuario, %s) > 0.2 or
                to_tsvector('spanish', s.nom_servicio) @@ to_tsquery('spanish', busqueda)  or similarity( s.nom_servicio, %s) > 0.2 or 
                to_tsvector('spanish', c.desc_categoria) @@ to_tsquery('spanish', busqueda)  or similarity( c.desc_categoria, %s) > 0.2 or
                to_tsvector('spanish', its.desc_item_servicio) @@ to_tsquery('spanish', busqueda)  or similarity( its.desc_item_servicio, %s) > 0.2
                    )
                       and s.cod_activo = 'S' and s.cod_pausado = 'N' AND (c2.cod_comuna = %s OR s.cod_es_nacional = 'S')
                GROUP  BY 1,2,3,4,5,6,7, s.dias_antelacion, desc_usuario, c2.cod_comuna
                ORDER  BY valoracion, desc_usuario"""

    cursor.execute(
        query,
        (
            '%' + unidecode(filtro.filtro) + '%',
            '%' + unidecode(filtro.filtro) + '%',
            '%' + unidecode(filtro.filtro) + '%',
            '%' + unidecode(filtro.filtro) + '%',
            '%' + unidecode(filtro.filtro) + '%',
            filtro.cod_comuna
        )
    )
    servicios = cursor.fetchall()
    conn.close()
    response.status_code = HTTP_200_OK
    print("SErvicios", servicios)
    return servicios


@router.post('/por_cod', response_model=RespPorCod, response_model_exclude_none=True)
async def get_by_cod_usuario_prestador(response: Response, servicio: ServicioCod):
    conn = PsqlConnection().conn
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """SELECT 
                s.*,
                false as favorito,
                to_json(array_agg(DISTINCT c.cod_comuna)) AS comunas,
                to_json(array_agg(DISTINCT c2.cod_categoria)) AS categorias
            FROM   usuario us
            JOIN servicio s on us.cod_usuario = s.cod_usuario
            LEFT JOIN servicio_comuna sc using(cod_servicio)
            LEFT JOIN comuna c ON c.cod_comuna = sc.cod_comuna
            JOIN categoria_servicio cs using(cod_servicio)
            JOIN categoria c2 using(cod_categoria)
            WHERE  s.cod_servicio = %s and s.cod_activo = 'S' and s.cod_pausado = 'N'
            GROUP  BY s.cod_servicio, s.cod_usuario, s.direccion, s.cod_retiro, us.nombre_usuario, us.cod_usuario,
                    s.cod_domicilio, s.cod_es_articulo, s.nom_servicio, s.desc_domicilio, s.cod_activo"""

    cursor.execute(
        query,
        (
            servicio.cod_servicio,
        )
    )
    serv_resp = cursor.fetchone()

    query = """SELECT itm.*, u.desc_unidad
                FROM item_servicio itm 
                JOIN unidad u on itm.cod_unidad = u.cod_unidad
                WHERE itm.cod_servicio = %s"""

    cursor.execute(
        query,
        (
            servicio.cod_servicio,
        )
    )
    serv_resp['items'] = cursor.fetchall()
    # print(serv_resp)
    query = """SELECT cod_horario_usuario,desde,hasta,
                       To_json(Array_agg(DISTINCT dia.*)) AS dias
                FROM   horario_usuario hu
                       join dia_horario_usuario dhu USING(cod_horario_usuario)
                       join dia USING(cod_dia)
                WHERE cod_usuario =  %s
                GROUP  BY 1,2,3 """

    cursor.execute(
        query,
        (
            servicio.cod_usuario,
        )
    )
    horarios = cursor.fetchall()
    resp = {"servicio": serv_resp, "horarios": horarios}
    conn.close()
    response.status_code = HTTP_200_OK
    return resp

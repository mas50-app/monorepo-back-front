from fastapi import APIRouter, Response, Request
from psycopg2.extras import RealDictCursor
from starlette.status import *
from bd_con.conexion import PsqlConnection
from dev_tools.notifications.app_notification import create_notification

router = APIRouter()


@router.post("/crear")
async def create_refund(response: Response, request: Request):
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    req_body = await request.body()
    print("Confirmacion de devolucion ---------", req_body)
    conn.close()
    response.status_code = HTTP_200_OK
    return req_body


@router.get("/crear")
async def create_refund(response: Response, request: Request):
    conn = PsqlConnection().conn
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    req_body = await request.body()
    print("Confirmacion de devolucion ---------", req_body)
    conn.close()
    response.status_code = HTTP_200_OK
    return req_body

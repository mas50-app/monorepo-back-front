from dotenv import load_dotenv
from jwt import encode, exceptions, decode
from datetime import datetime, timedelta
import os
from fastapi.responses import JSONResponse

load_dotenv()


def fecha_exp(dias: int):
    fecha_actual = datetime.now()
    nueva_fecha = fecha_actual + timedelta(dias)
    return nueva_fecha


def generar_token(data: dict):
    token = encode(payload={**data, 'exp': fecha_exp(2)}, key=os.environ.get('SECRET_KEY'), algorithm='HS256')
    return token


def validar_token(token, output=False):
    try:
        if output:
            return decode(token, key=os.environ.get('SECRET_KEY'), algorithms=['HS256'])
        decode(token, key=os.environ.get('SECRET_KEY'), algorithms=['HS256'])
    except exceptions.DecodeError:
        return JSONResponse(content={'mensaje': 'Token Invalido'}, status_code=401)
    except exceptions.ExpiredSignatureError:
        return JSONResponse(content={'mensaje': 'Token Expirado'}, status_code=401)


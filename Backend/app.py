from typing import Optional

from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from pydantic import BaseModel

from dev_tools.simple_json_response import SimpleJSONResponse
from routes.app_routes import usuario_route, auth_route, banco_route, tipo_antecedente_route, servicio_route, \
    unidad_route, \
    comuna_route, tipo_cuenta_bancaria_route, cuenta_bancaria_route, evaluacion_route, pago_route, \
    movimiento_bancario_route, documento_route, estado_documento_route, item_route, imagen_route, imagen_server_route, \
    flow_payment_confirm_route, notificacion_route, direccion_route, app_version_route, categoria_route, \
    servicio_sin_token_route, courier_route
from routes.backOffice_routes import auth, register, tipo_personal, usuarios, prestadores, servicios, dashboard, \
    flow_refund_confirm, devoluciones, liquidaciones, documentos, personal, categoria, region

load_dotenv()

app = FastAPI(
    title="+50 Api",
    description="Endpoints para aplicación +50\n Desarrollado por OsmaniCR",
    version="1.0.0",
    default_response_class=SimpleJSONResponse
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


class Error(BaseModel):
    error: Optional[str]


@app.post("/api/v1/error")
async def get_error(error: Error):
    print("-------ERROR", error)
    return True


# @app.get("/test")
# async def test():
#     return "Test"

# ###---------------------------------------------------------------------------------------------### #
# ###---------------------------------------------------------------------------------------------### #
# ###--------------------------------- Servicios para App ---------------------------------### #
# ###---------------------------------------------------------------------------------------------### #
# ###---------------------------------------------------------------------------------------------### #

# -----------------------------------Rutas App Version-----------------------------------
app.include_router(app_version_route.router, prefix="/api/v1/app", tags=["App | Rutas App Version "])

# -----------------------------------Rutas Relacionadas Con Autenticacion-----------------------------------
app.include_router(usuario_route.router, prefix="/api/v1/usuarios", tags=["App | Rutas de Usuarios"])
app.include_router(auth_route.router, prefix="/api/v1/auth", tags=["App | Rutas de Authentication"])

# -----------------------------------Rutas Relacionadas Con Bancos-----------------------------------
app.include_router(banco_route.router, prefix="/api/v1/bancos", tags=["App | Rutas de Bancos"])
app.include_router(tipo_cuenta_bancaria_route.router, prefix="/api/v1/tipos_cuentas_bancarias", tags=["App | Rutas de Tipos de Cta Bancaria"])
app.include_router(cuenta_bancaria_route.router, prefix="/api/v1/cuentas_bancarias", tags=["App | Rutas de Cuentas Bancarias"])

# -----------------------------------Rutas Relacionadas Con Servicios o Talentos-----------------------------------
app.include_router(servicio_route.router, prefix="/api/v1/servicios", tags=["App | Rutas de Servicios"])
app.include_router(servicio_sin_token_route.router, prefix="/api/v1/servicios_st", tags=["App | Rutas de Servicios Abiertos"])

# -----------------------------------Rutas Relacionadas Con Pagos y Movimientos bancarios-----------------------------------
app.include_router(pago_route.router, prefix="/api/v1/pagos", tags=["App | Rutas de Pagos"])
app.include_router(movimiento_bancario_route.router, prefix="/api/v1/movimientos_bancarios", tags=["App | Rutas de Movimientos Bancarios"])

# -----------------------------------Rutas Relacionadas Con Documentos y Ventas-----------------------------------
app.include_router(documento_route.router, prefix="/api/v1/documentos", tags=["App | Rutas de Docuementos"])
app.include_router(estado_documento_route.router, prefix="/api/v1/estados_documento", tags=["App | Rutas de Estados Documento"])
app.include_router(direccion_route.router, prefix="/api/v1/direcciones", tags=["App | Rutas de Direcciones"])

# -----------------------------------Rutas Relacionadas Con Evaluaciones de servicios-----------------------------------
app.include_router(evaluacion_route.router, prefix="/api/v1/evaluaciones", tags=["App | Rutas de Evaluaciones"])

# -----------------------------------Rutas Maestros Varios-----------------------------------
app.include_router(tipo_antecedente_route.router, prefix="/api/v1/tipos_antecedentes", tags=["App | Rutas de Tipos Antecedente"])
app.include_router(unidad_route.router, prefix="/api/v1/unidades", tags=["App | Rutas de Unidades"])
app.include_router(comuna_route.router, prefix="/api/v1/comunas", tags=["App | Rutas de Comunas"])
app.include_router(categoria_route.router, prefix="/api/v1/categorias", tags=["App | Rutas de Categorias"])


# -----------------------------------Rutas Manejo de Items-----------------------------------
app.include_router(item_route.router, prefix="/api/v1/items", tags=["App | Rutas de Items"])

# -----------------------------------Rutas Manejo de Notificaciones-----------------------------------
app.include_router(notificacion_route.router, prefix="/api/v1/notificaciones", tags=["App | Rutas de Notificaciones"])

# -----------------------------------Rutas Manejo de Imagenes-----------------------------------
app.include_router(imagen_route.router, prefix="/api/v1/imagenes", tags=["App | Rutas de imagenes"])
app.include_router(imagen_server_route.router, prefix="/api/v1/imagenes_server", tags=["App | Rutas de Imagen Server"])


# -----------------------------------Rutas Manejo Despachos-----------------------------------
app.include_router(courier_route.router, prefix="/api/v1/couriers", tags=["App | Rutas de Couriers"])


# ###---------------------------------------------------------------------------------------------### #
# ###---------------------------------------------------------------------------------------------### #
# ###--------------------------------- Servicios para BackOffice ---------------------------------### #
# ###---------------------------------------------------------------------------------------------### #
# ###---------------------------------------------------------------------------------------------### #

# -----------------------------------Rutas Relacionadas Con El Login y Creacion de Personal-----------------------------------
app.include_router(auth.router, prefix="/api/v1/back_office/auth", tags=["BackOffice | Rutas de Authentication"])
app.include_router(register.router, prefix="/api/v1/back_office/auth", tags=["BackOffice | Rutas de Register"])
app.include_router(tipo_personal.router, prefix="/api/v1/back_office/tipos_personal", tags=["BackOffice | Rutas de Tipos Personal"])


# -----------------------------------Rutas Relacionadas Con Devoluciones-----------------------------------
app.include_router(devoluciones.router, prefix="/api/v1/back_office/devoluciones", tags=["BackOffice | Rutas de Devoluciones"])


# -----------------------------------Rutas Relacionadas Con Categorías-----------------------------------
app.include_router(categoria.router, prefix="/api/v1/back_office/categorias", tags=["BackOffice | Rutas de Categorías"])

# -----------------------------------Rutas Relacionadas Con Regiones-----------------------------------
app.include_router(region.router, prefix="/api/v1/back_office/regiones", tags=["BackOffice | Rutas de Regiones"])

# -----------------------------------Rutas Relacionadas Con Liquidaciones-----------------------------------
app.include_router(liquidaciones.router, prefix="/api/v1/back_office/liquidaciones", tags=["BackOffice | Rutas de Liquidaciones"])

# -----------------------------------Rutas Relacionadas Con El Dashboard-----------------------------------
app.include_router(app_version_route.router, prefix="/api/v1/back_office/app", tags=["BackOffice | Rutas App Version "])
app.include_router(usuarios.router, prefix="/api/v1/back_office/usuarios", tags=["BackOffice | Rutas de Usuarios"])
app.include_router(prestadores.router, prefix="/api/v1/back_office/prestadores", tags=["BackOffice | Rutas de Prestadores"])
app.include_router(servicios.router, prefix="/api/v1/back_office/prestaciones", tags=["BackOffice | Rutas de Prestaciones"])
app.include_router(dashboard.router, prefix="/api/v1/back_office/dashboard", tags=["BackOffice | Rutas de Dashboard"])
app.include_router(documentos.router, prefix="/api/v1/back_office/documentos", tags=["BackOffice | Rutas de Documentos"])
app.include_router(banco_route.router, prefix="/api/v1/back_office/bancos", tags=["BackOffice | Rutas de Bancos"])
app.include_router(tipo_cuenta_bancaria_route.router, prefix="/api/v1/back_office/tipos_cuentas_bancarias", tags=["BackOffice | Rutas de Tipos de Cta Bancaria"])
app.include_router(comuna_route.router, prefix="/api/v1/back_office/comunas", tags=["BackOffice | Rutas de Comunas"])
app.include_router(personal.router, prefix="/api/v1/back_office/personal", tags=["BackOffice | Rutas de Personal"])
app.include_router(courier_route.router, prefix="/api/v1/back_office/couriers", tags=["BackOffice | Rutas de Couriers"])

# ###---------------------------------------------------------------------------------------------### #
# ###---------------------------------------------------------------------------------------------### #
# ###---------------------------------------------------------------------------------------------### #
# ###--------------------------------- Servicios para Pasarela de Pagos --------------------------### #
# ###---------------------------------------------------------------------------------------------### #
# ###---------------------------------------------------------------------------------------------### #
# ###---------------------------------------------------------------------------------------------### #


# -----------------------------------Rutas Relacionadas a creación de  Pagos-----------------------------------
app.include_router(flow_payment_confirm_route.router, prefix="/api/v1/flow_payment_confirm", tags=["Rutas Libres"])
app.include_router(flow_refund_confirm.router, prefix="/api/v1/flow_refund_confirm", tags=["Rutas Libres"])


if __name__ == '__main__':
    uvicorn.run(app, host=os.environ.get('HOST'), port=int(os.environ.get('PORT')))

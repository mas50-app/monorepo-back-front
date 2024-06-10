from fastapi import Request, Response
from fastapi.routing import APIRoute, JSONResponse
from dev_tools.json_web_token import validar_token
from typing import Callable


class VerificaRutaToken(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route = super().get_route_handler()

        async def verify_token_middleware(request: Request) -> Response:
            try:
                token = request.headers['Authorization'].split(" ")[1]
            except:
                return JSONResponse(content={"mensaje": "Falta Token en Headers"}, status_code=403)
            # validation_reponse = validar_token(token, output=False)
            if validar_token(token) is None:
                return await original_route(request)
            return validar_token(token)

        return verify_token_middleware

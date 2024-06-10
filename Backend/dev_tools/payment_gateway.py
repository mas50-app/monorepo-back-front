import hashlib
import hmac
import urllib.parse
from typing import Dict
import requests
from dotenv import load_dotenv
import os
from models.payment_gateway_models.payment_models import PaymentCreate, RefundCreate

load_dotenv()


class Payment:
    def __init__(self):
        if os.environ.get("ENV") == 'dev':
            self.API_URL = os.environ.get("FLOW_DEV_API_URL")
            self.API_KEY = os.environ.get("DEV_FLOW_API_KEY")
            self.API_SECRET = os.environ.get("DEV_FLOW_SECRET_KEY")
        else:
            self.API_URL = os.environ.get("FLOW_API_URL")
            self.API_KEY = os.environ.get("FLOW_API_KEY")
            self.API_SECRET = os.environ.get("FLOW_SECRET_KEY")

    def create_signature(self, params: Dict):
        sorted_data = ''.join([f'{k}{v}' for k, v in sorted(params.items()) if k != 's'])
        hash_string = hmac.new(self.API_SECRET.encode(), sorted_data.encode(), hashlib.sha256).hexdigest()
        return hash_string

    def create_order(self, payment_data: PaymentCreate):
        payment_data.apiKey = self.API_KEY
        params = payment_data.dict(exclude_none=True)
        signature = self.create_signature(params=params)

        # Agregar la firma al diccionario de parámetros
        payment_data.s = signature

        payload = payment_data.dict(exclude_none=True)
        headers = {"content-type": "application/x-www-form-urlencoded"}
        resp = requests.request(
            "POST",
            self.API_URL + "/payment/create",
            data=urllib.parse.urlencode(payload),
            headers=headers
        )
        return resp

    def create_refund(self, refund_data: RefundCreate):
        refund_data.apiKey = self.API_KEY
        params = refund_data.dict(exclude_none=True)
        signature = self.create_signature(params=params)
        refund_data.s = signature
        payload = refund_data.dict(exclude_none=True)
        headers = {"content-type": "application/x-www-form-urlencoded"}
        resp = requests.request(
            "POST",
            self.API_URL + "/refund/create",
            data=urllib.parse.urlencode(payload),
            headers=headers
        )
        return resp

    def cancel_refund(self, token):
        params = {
            "apiKey": self.API_KEY,
            "token": token
        }
        signature = self.create_signature(params=params)
        params["s"] = signature
        headers = {"content-type": "application/x-www-form-urlencoded"}
        resp = requests.request(
            "POST",
            self.API_URL + "/refund/cancel",
            data=urllib.parse.urlencode(params),
            headers=headers
        )
        return resp

    def get_refund_status(self, token):
        params = {
            "apiKey": self.API_KEY,
            "token": token
        }
        signature = self.create_signature(params=params)
        params["s"] = signature
        headers = {"content-type": "application/x-www-form-urlencoded"}
        resp = requests.request(
            "GET",
            self.API_URL + "/refund/getStatus"+ f"?{urllib.parse.urlencode(params)}",
            # data=urllib.parse.urlencode(params),
            headers=headers
        )
        return resp


if __name__ == "__main__":
    payment = Payment()
    url_confirmation = "http://api/v1/flow_refund_confirm/crear"
    payment_d = {
        "refundCommerceOrder": "123456",
        "flowTrxId": "1575525",
        # "commerceTrxId": "1572955",
        "amount": 500,
        "receiverEmail": "osmanicasanueva@gmail.com",
        "urlCallBack": url_confirmation
    }
    # ri = payment.create_refund(refund_data=RefundCreate(**payment_d))
    tokens = [
        "3F85DBD6022EA268AB311647541B3D3695C267FA",
        "E0520F66673FD909BBABC069267753F1825C3ECE",
        "9C919FC8992EBE44C4AAFA4098C8CA675CCC3DAE",
        "8E297BF628758ADBFE199C371F14EBB7AC9E263P",
        "246FBAEDA8501210AB4EFC1501C921226580A5FT",
    ]
    for token in tokens:

        re = payment.get_refund_status(token=token)
        print(re.json())


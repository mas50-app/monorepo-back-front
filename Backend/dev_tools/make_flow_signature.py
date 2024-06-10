import hmac
import hashlib
from typing import Dict, Any


def make_flow_signature(secret: str, params: Dict):
    sorted_data = ''.join([f'{k}{v}' for k, v in sorted(params.items()) if k != 's'])
    hash_string = hmac.new(secret.encode(), sorted_data.encode(), hashlib.sha256).hexdigest()
    print("Esta será la firma  ", sorted_data)
    return hash_string

from typing import Dict, Any
import hmac
import hashlib
import time
from urllib.parse import urlencode

class BinanceAuth:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret

    @staticmethod
    def get_timestamp() -> int:
        return int(time.time() * 1000)

    def generate_signature(self, query_string: str) -> str:
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def get_auth_headers(self) -> Dict[str, str]:
        return {"X-MBX-APIKEY": self.api_key}
    
##cleanup request params
    def encoded_string(self, query, special=False):
        if special:
            return urlencode(query).replace("%40", "@").replace("%27", "%22")
        else:
            return urlencode(query, True).replace("%40", "@")

    def cleanNoneValue(self, d) -> dict:
        out = {}
        for k in d.keys():
            if d[k] is not None:
                out[k] = d[k]
        return out

    def prepare_params(self, params, special=False):
        return self.encoded_string(self.cleanNoneValue(params), special)


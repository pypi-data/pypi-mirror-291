from pydantic import BaseModel
from ipaddress import IPv4Address


class Config(BaseModel):
    port: int = 8080
    host: IPv4Address = '127.0.0.1'

    onebot_access_token: str = ''

    lagrange_path: str = 'Lagrange'

    lagrange_auto_start: bool = True
    lagrange_auto_install: bool = True

    lagrange_max_cache_log: int = 500

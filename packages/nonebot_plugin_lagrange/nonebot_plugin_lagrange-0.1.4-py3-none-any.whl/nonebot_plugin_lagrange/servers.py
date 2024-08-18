from json import dumps
from pathlib import Path

from nonebot import get_driver
from nonebot.log import logger
from nonebot.drivers import HTTPServerSetup, ASGIMixin, Response, Request, URL

from . import globals
# from .manager import manager


async def static(request: Request):
    file_name = 'index.html' if request.url.name == 'lagrange' else request.url.name
    file_path = (Path('webui') / file_name)
    if not file_path.exists():
        return Response(404, content='WebUI was never installed.')
    with file_path.open('r', encoding='utf-8') as file:
        return Response(200, content=file.read())


async def api_start(request: Request):
    if request.headers.get('token') != '123':
        return Response(403)
    return Response(200, content=dumps(request.json))


def setup_servers():
    if isinstance((driver := get_driver()), ASGIMixin):
        servers = (
            HTTPServerSetup(URL('/lagrange'), 'GET', 'page', static),
            HTTPServerSetup(URL('/lagrange/index.js'), 'GET', 'page', static),
            HTTPServerSetup(URL('/lagrange/index.css'), 'GET', 'page', static),
            HTTPServerSetup(URL('/lagrange/api/start'), 'POST', 'page', api_start),
        )
        for server in servers:
            driver.setup_http_server(server)
        logger.success('载入 WebUi 成功！请保管好下方的链接，以供使用。')
        color_logger = logger.opt(colors=True)
        color_logger.info(
            F'WebUi <yellow><b>http://{driver.config.host}:{driver.config.port}'
            F'/webui?token={"1234"}</b></yellow>'
        )
        return None
    logger.error('当前驱动不支持 Http 服务器！载入 WebUi 失败，请检查驱动是否正确。')

import platform
import tarfile
import time
from io import BytesIO
from httpx import AsyncClient
from subprocess import Popen, PIPE

from nonebot.log import logger

from . import paths
from .utils import parse_platform


def extract_lagrange(file: BytesIO):
    try:
        with tarfile.open(fileobj=file) as zip_file:
            for member in zip_file.getmembers():
                if member.isfile():
                    with zip_file.extractfile(member) as file:
                        file_name = file.name.split('/')[-1]
                        with open(paths.data_path / file_name, 'wb') as target_file:
                            target_file.write(file.read())
                            return True
    except Exception as error:
        logger.error(F'Lagrange.Onebot 解压失败！错误信息 {error}')
    return False


def generate_default_settings():
    path = next(paths.data_path.rglob('Lagrange.OneBot*'))
    path.chmod(0x755)
    task = Popen(str(path.absolute()), stdout=PIPE, cwd=str(paths.data_path))
    while not tuple(paths.data_path.rglob('appsettings.json')):
        time.sleep(2)
    task.terminate()


async def update():
    logger.info('Lagrange.Onebot 正在更新……')
    if paths.lagrange_path is not None:
        paths.lagrange_path.unlink()
    if paths.appsettings_path is not None:
        paths.appsettings_path.unlink()
    return await install()


async def install():
    if paths.lagrange_path is not None:
        logger.warning('检测到 Lagrange.Onebot 已安装，无需再次安装！')
        return True
    system, architecture = parse_platform()
    logger.info(F'检测到当前的系统架构为 {system} {architecture} 正在下载对应的安装包……')
    if response := await download_github(
            'https://github.com/LagrangeDev/Lagrange.Core/releases/download/'
            F'nightly/Lagrange.OneBot_{system}-{architecture}_net8.0_SelfContained.tar.gz'
    ):
        logger.success(F'Lagrange.Onebot 下载成功！正在安装……')
        if extract_lagrange(response):
            generate_default_settings()
            paths.update_file_paths()
            logger.success('Lagrange.Onebot 安装成功！')
            return True
    logger.error('Lagrange.Onebot 安装失败！')
    return False


async def download_github(url: str):
    download_bytes = BytesIO()
    async with AsyncClient() as client:
        try:
            async with client.stream('GET', 'https://mirror.ghproxy.com/' + url) as stream:
                if stream.status_code != 200:
                    return False
                async for chunk in stream.aiter_bytes():
                    download_bytes.write(chunk)
                download_bytes.seek(0)
                return download_bytes
        except Exception as error:
            logger.error(F'Lagrange.Onebot 下载失败！错误信息 {error}')
            return False

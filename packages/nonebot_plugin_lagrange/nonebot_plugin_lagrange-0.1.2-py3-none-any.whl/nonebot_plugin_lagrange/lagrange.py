import asyncio
from asyncio.subprocess import PIPE, Process
from pathlib import Path
from threading import Thread
from json import dump, load

from nonebot.log import logger
from nonebot.plugin import get_plugin_config

from . import paths
from .utils import parse_log_level
from .config import Config
from .network import generate_default_settings, install


class Lagrange(Thread):
    cache: list = []

    path: Path = None
    task: Process = None
    config: Config = None

    def __init__(self):
        Thread.__init__(self, name='Lagrange', daemon=True)
        self.config = get_plugin_config(Config)
        self.path = Path(self.config.lagrange_path)
        if paths.lagrange_path and self.config.lagrange_auto_start:
            logger.info('Lagrange.Onebot 已经安装，正在启动……')
            self.start()
        elif (not paths.lagrange_path) and self.config.lagrange_auto_install:
            logger.info('Lagrange.Onebot 未安装，正在安装……')
            asyncio.run(install())

    def stop(self):
        if self.task:
            self.task.terminate()

    def logout(self):
        for file_path in self.path.rglob('*'):
            if file_path.name != 'appsettings.json':
                file_path.unlink()
        self.stop()

    def run(self):
        asyncio.run(self.run_lagrange())

    async def run_lagrange(self):
        self.update_config()
        self.task = await asyncio.create_subprocess_exec(str(paths.lagrange_path), stdout=PIPE, cwd=self.path)
        logger.success('Lagrange.Onebot 启动成功！请扫描目录下的图片或控制台中的二维码登录。')
        while self.task:
            if self.task.returncode is not None:
                logger.info('Lagrange.Onebot 已退出！如若没有正常使用，请检查日志。')
                break
            if line := await self.task.stdout.readline():
                line = line.decode('Utf-8').strip()
                self.cache.append(line)
                if len(self.cache) > self.config.lagrange_max_cache_log:
                    self.cache.pop(0)
                if line[0] in ('█', '▀'):
                    logger.info(line)
                    continue
                elif log_level := parse_log_level(line):
                    if log_level == 'WARNING':
                        logger.warning(line)
                        continue
                    logger.debug(line)
                continue
            self.stop()

    def update_config(self):
        if not self.path.exists():
            self.path.mkdir()
        config_path = (self.path / 'appsettings.json')
        if paths.appsettings_path is None:
            generate_default_settings()
            paths.update_file_paths()
        with paths.appsettings_path.open('r', encoding='Utf-8') as file:
            lagrange_config = load(file)
        lagrange_config['Implementations'][0]['Port'] = self.config.port
        lagrange_config['Implementations'][0]['Host'] = str(self.config.host)
        lagrange_config['Implementations'][0]['AccessToken'] = self.config.onebot_access_token
        with config_path.open('w', encoding='Utf-8') as file:
            dump(lagrange_config, file)
            logger.success('Lagrange.Onebot 配置文件更新成功！')
            return True

import asyncio

from nonebot.log import logger
from nonebot.plugin import get_plugin_config

from . import globals
from .config import Config
from .lagrange import Lagrange
from .network import install


class Manager:
    lagrange: list = []

    config: Config = None

    def __init__(self):
        self.config = get_plugin_config(Config)
        for lagrange_name in self.config.lagrange_path.rglob('*'):
            if lagrange_name.is_dir():
                self.lagrange.append(Lagrange(self.config, lagrange_name.name))
        if globals.lagrange_path and self.config.lagrange_auto_start:
            logger.info('Lagrange.Onebot 已经安装，正在启动……')
            if not tuple(self.config.lagrange_path.rglob('*')):
                self.create_lagrange('Default', False)
        elif (not globals.lagrange_path) and self.config.lagrange_auto_install:
            logger.info('Lagrange.Onebot 未安装，正在安装……')
            asyncio.run(install())

    def run(self):
        for lagrange in self.lagrange:
            asyncio.create_task(lagrange.run())

    def stop(self):
        for lagrange in self.lagrange:
            lagrange.stop()

    def create_lagrange(self, lagrange_name: str, auto_run: bool = True):
        if not self.config.lagrange_path.exists():
            self.config.lagrange_path.mkdir()
        if not globals.lagrange_path or not self.config.lagrange_auto_install:
            logger.error('Lagrange.Onebot 未安装，无法创建 Lagrange')
            return False
        elif lagrange_name in (lagrange.name for lagrange in self.lagrange):
            logger.warning(F'Lagrange {lagrange_name} 已存在，无法重复创建')
            return False
        lagrange = Lagrange(self.config, lagrange_name)
        self.lagrange.append(lagrange)
        if auto_run is True:
            asyncio.create_task(lagrange.run())
        return True


manager = Manager()

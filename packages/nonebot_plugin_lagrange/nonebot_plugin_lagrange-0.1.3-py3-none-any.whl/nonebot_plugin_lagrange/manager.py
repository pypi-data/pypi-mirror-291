import asyncio
from asyncio import AbstractEventLoop, CancelledError
from threading import Thread

from nonebot.log import logger
from nonebot.plugin import get_plugin_config

from . import paths
from .config import Config
from .lagrange import Lagrange
from .network import install


class Manager(Thread):
    lagrange: list = []

    config: Config = None
    event_loop: AbstractEventLoop = None

    def __init__(self):
        Thread.__init__(self, name='Lagrange', daemon=True)
        self.config = get_plugin_config(Config)
        for lagrange_name in self.config.lagrange_path.rglob('*'):
            if lagrange_name.is_dir():
                self.lagrange.append(Lagrange(self.config, lagrange_name.name))
        if paths.lagrange_path and self.config.lagrange_auto_start:
            logger.info('Lagrange.Onebot 已经安装，正在启动……')
            if not tuple(self.config.lagrange_path.rglob('*')):
                self.create_lagrange('Default')
            else: self.start()
        elif (not paths.lagrange_path) and self.config.lagrange_auto_install:
            logger.info('Lagrange.Onebot 未安装，正在安装……')
            asyncio.run(install())

    def run(self):
        self.event_loop = asyncio.new_event_loop()
        if not self.config.lagrange_path.exists():
            self.config.lagrange_path.mkdir()
        for lagrange in self.lagrange:
            self.event_loop.create_task(lagrange.run())
        self.event_loop.run_forever()

    def stop(self):
        for lagrange in self.lagrange:
            lagrange.stop()
        self.event_loop.stop()

    def create_lagrange(self, lagrange_name: str):
        if not paths.lagrange_path or not self.config.lagrange_auto_install:
            logger.error('Lagrange.Onebot 未安装，无法创建 Lagrange')
            return False
        elif lagrange_name in (lagrange.name for lagrange in self.lagrange):
            logger.warning(F'Lagrange {lagrange_name} 已存在，无法重复创建')
            return False
        lagrange = Lagrange(self.config, lagrange_name)
        asyncio.run(lagrange.run())
        self.lagrange.append(lagrange)
        return True

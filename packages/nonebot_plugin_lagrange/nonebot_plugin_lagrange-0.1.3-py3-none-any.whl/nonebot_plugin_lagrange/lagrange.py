import asyncio
from asyncio.subprocess import Process, PIPE
from pathlib import Path
from json import dump, load

import nonebot
from nonebot.log import logger

from . import paths
from .utils import parse_log_level
from .config import Config
from .network import generate_default_settings


class Lagrange:
    cache: list = []

    name: str = None
    path: Path = None
    task: Process = None
    config: Config = None

    def __init__(self, config: Config, name: str):
        self.name = name
        self.config = config
        self.path = (self.config.lagrange_path / name)

    def rename(self, name: str):
        self.name = name
        self.path = self.path.rename(name)

    def stop(self):
        if self.task is not None:
            self.task.terminate()

    def logout(self):
        if self.task is None:
            for file_path in self.path.rglob('*'):
                if file_path.name != 'appsettings.json':
                    file_path.unlink()

    async def run(self):
        self.update_config()
        self.task = await asyncio.create_subprocess_exec(str(paths.lagrange_path), stdout=PIPE, cwd=self.path)
        self.log('SUCCESS', 'Lagrange.Onebot 启动成功！请扫描目录下的图片或控制台中的二维码登录。')
        async for line in self.task.stdout:
            if not line: self.stop()
            line = line.decode('Utf-8').strip()
            self.cache.append(line)
            if len(self.cache) > self.config.lagrange_max_cache_log:
                self.cache.pop(0)
            if line[0] in ('█', '▀'):
                self.log('INFO', line)
                continue
            elif log_level := parse_log_level(line):
                if log_level == 'WARNING':
                    self.log('WARNING', line)
                    continue
                self.log('DEBUG', line)
            continue
        self.task = None
        self.log('INFO', 'Lagrange.Onebot 已退出！如若没有正常使用，请检查日志。')

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
            self.log('SUCCESS', 'Lagrange.Onebot 配置文件更新成功！')
            return True

    def log(self, level: str, content: str):
        content = F'[{self.name}] {content}'
        logger.log(level, content)

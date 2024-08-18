from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata

from .config import Config
from .lagrange import Lagrange
from .paths import update_file_paths

__plugin_meta__ = PluginMetadata(
    name='lagrange',
    description='A simple Lagrange.OneBot manager plugin.',

    usage='Lagrange.OneBot manager plugin. Can use command to manage it.',

    type='application',
    # 发布必填，当前有效类型有：`library`（为其他插件编写提供功能），`application`（向机器人用户提供功能）。

    homepage='https://www.github.com/Lonely-Sails/nonebot-plugin-lagrange',
    # 发布必填。

    config=Config,
    # 插件配置项类，如无需配置可不填写。

    supported_adapters={'~onebot.v11'},
    # 支持的适配器集合，其中 `~` 在此处代表前缀 `nonebot.adapters.`，其余适配器亦按此格式填写。
    # 若插件可以保证兼容所有适配器（即仅使用基本适配器功能）可不填写，否则应该列出插件支持的适配器。
)

update_file_paths()

lagrange = Lagrange()

stop_matcher = on_command('lagrange stop', aliases={'关闭拉格兰', '关闭'}, permission=SUPERUSER)
start_matcher = on_command('lagrange start', aliases={'启动拉格兰', '启动'}, permission=SUPERUSER)
status_matcher = on_command('lagrange status', aliases={'拉格兰状态', '状态'}, permission=SUPERUSER)


@stop_matcher.handle()
async def _():
    if lagrange.task:
        lagrange.stop()
        await stop_matcher.finish('Lagrange.OneBot 已关闭。')
    await stop_matcher.reject('Lagrange.OneBot 已经处于关闭状态！')


@start_matcher.handle()
async def _():
    if not lagrange.task:
        lagrange.start()
        await start_matcher.finish('Lagrange.OneBot 已启动！')
    await stop_matcher.reject('Lagrange.OneBot 已经启动过了，无法再次启动！')


@status_matcher.handle()
async def _():
    await status_matcher.finish('Lagrange 当前状态为 ' + '开启' if lagrange.task else '关闭')

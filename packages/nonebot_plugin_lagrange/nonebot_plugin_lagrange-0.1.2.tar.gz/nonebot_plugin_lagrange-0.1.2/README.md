<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-lagrange

_✨ 一款简化 Lagrange.OneBot 使用的插件。 ✨_

</div>

## 📖 介绍

本插件旨在使用户能够简单的使用 Lagrange.OneBot 来部署机器人。目前实现的功能有：

- 通过指令控制
- 自动配置使其连接上 NoneBot
- 根据系统自动安装合适的 Lagrange.OneBot

## 💿 安装

你可以使用 `pip3 install nonebot-plugin-lagrange` 来安装此插件。

## ⚙️ 配置

在 NoneBot2 项目的`.env`文件中添加下表中的必填配置

|          配置项           | 必填 |   默认值    |            说明             |
|:----------------------:|:--:|:--------:|:-------------------------:|
|     lagrange_path      | 否  | Lagrange | Lagrange.OneBot 的安装和运行目录。 |
|  lagrange_auto_start   | 否  |   True   |  是否在检测到有安装 Lgr 的情况下自动启动。  |
| lagrange_auto_install  | 否  |   True   |    是否在未安装 Lgr 的情况自动安装     |
| lagrange_max_cache_log | 否  |   500    |         最大缓存多少行日志         |

## 🎉 使用

### 指令表

|     指令     | 权限 | 需要@ | 范围 |            说明            |
|:----------:|:--:|:---:|:--:|:------------------------:|
| 启动拉格兰 / 启动 | 主人 |  否  | 无  |    启动 Lagrange.OneBot    |
| 关闭拉格兰 / 关闭 | 主人 |  否  | 无  |    关闭 Lagrange.OneBot    |
| 拉格兰状态 / 状态 | 主人 |  否  | 无  | 查看当前 Lagrange.OneBot 的状态 |

当然，你也可以在代码中使用：

```python
from nonebot import require

require('nonebot_plugin_lagrange')
from nonebot_plugin_lagrange import lagrange

# 启动 LGR
lagrange.start()

# 停止 LGR
lagrange.stop()

# 安装 LGR
lagrange.install()

```

## 🫓 大饼

- 使用 WebUi 来控制 Lagrange.
- 实现多账号登录。

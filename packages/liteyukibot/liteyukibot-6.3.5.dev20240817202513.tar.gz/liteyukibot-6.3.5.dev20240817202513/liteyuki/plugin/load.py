# -*- coding: utf-8 -*-
"""
Copyright (C) 2020-2024 LiteyukiStudio. All Rights Reserved 

@Time    : 2024/7/23 下午11:59
@Author  : snowykami
@Email   : snowykami@outlook.com
@File    : load.py
@Software: PyCharm
"""
import os
import traceback
from pathlib import Path
from typing import Optional

from liteyuki.log import logger
from liteyuki.plugin.model import Plugin, PluginMetadata
from importlib import import_module

from liteyuki.utils import path_to_module_name

_plugins: dict[str, Plugin] = {}

__all__ = [
        "load_plugin",
        "load_plugins",
]


def load_plugin(module_path: str | Path) -> Optional[Plugin]:
    """加载单个插件，可以是本地插件或是通过 `pip` 安装的插件。

    参数:
        module_path: 插件名称 `path.to.your.plugin`
        或插件路径 `pathlib.Path(path/to/your/plugin)`
    """
    module_path = path_to_module_name(Path(module_path)) if isinstance(module_path, Path) else module_path
    try:
        module = import_module(module_path)
        _plugins[module.__name__] = Plugin(
            name=module.__name__,
            module=module,
            module_name=module_path,
            metadata=module.__dict__.get("__plugin_metadata__", None)
        )
        display_name = module.__name__.split(".")[-1]
        if module.__dict__.get("__plugin_meta__"):
            metadata: "PluginMetadata" = module.__dict__["__plugin_meta__"]
            display_name = f"{metadata.name}({module.__name__.split('.')[-1]})"
        logger.opt(colors=True).success(
            f'Succeeded to load liteyuki plugin "<y>{display_name}</y>"'
        )
        return _plugins[module.__name__]

    except Exception as e:
        logger.opt(colors=True).success(
            f'Failed to load liteyuki plugin "<r>{module_path}</r>"'
        )
        traceback.print_exc()
        return None


def load_plugins(*plugin_dir: str) -> set[Plugin]:
    """导入文件夹下多个插件

    参数:
        plugin_dir: 文件夹路径
    """
    plugins = set()
    for dir_path in plugin_dir:
        # 遍历每一个文件夹下的py文件和包含__init__.py的文件夹，不递归
        for f in os.listdir(dir_path):
            path = Path(os.path.join(dir_path, f))

            module_name = None
            if os.path.isfile(path) and f.endswith('.py') and f != '__init__.py':
                module_name = f"{path_to_module_name(Path(dir_path))}.{f[:-3]}"

            elif os.path.isdir(path) and os.path.exists(os.path.join(path, '__init__.py')):
                module_name = path_to_module_name(path)

            if module_name:
                load_plugin(module_name)
                if _plugins.get(module_name):
                    plugins.add(_plugins[module_name])
    return plugins

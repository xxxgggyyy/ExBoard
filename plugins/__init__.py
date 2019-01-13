import os
import importlib

#导入插件包，主要就是执行其中的注册功能

for root, dirs, files in os.walk("./plugins"):
    if '__pycache__' in dirs:
        dirs.remove("__pycache__")
    for pkgName in dirs:
        module = importlib.import_module("plugins."+pkgName)
    break
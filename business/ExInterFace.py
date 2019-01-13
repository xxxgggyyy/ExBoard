from .Board import Board
from .Plugin import Plugin

class ExInterFace:

    __main_window = None

    __plugins = []

    __repeat_boardname = []

    @staticmethod
    def register(plugin):
        if isinstance(plugin, Plugin):
            ExInterFace.__plugins.append(plugin)
        else:
            raise TypeError("plugin object must inherit plugin.Plugin")

    @staticmethod
    def getPlugins():  # 获取注册了的插件
        return ExInterFace.__plugins

    @staticmethod
    def init(mainWnd):
        ExInterFace.__main_window = mainWnd
        # 在这里完成插件的加载
        import plugins  # 执行一下插件包里的__init__的register代码 注册到Exinterface中
        #将插件注册到mainWindow中
        ExInterFace.__main_window.registerPulgins(ExInterFace.__plugins)

    @staticmethod
    def addBorad(name):
        #不允许有重复的名字
        #统计重复次数
        reNum = ExInterFace.__repeat_boardname.count(name)
        ExInterFace.__repeat_boardname.append(name)
        if reNum != 0:
            name += (" "+str(reNum))
        board = Board(name, ExInterFace.__main_window)
        return ExInterFace.__main_window.addBoard(board)

    @staticmethod
    def removeBoard(b):
        ExInterFace.__main_window.removeBoard(b)
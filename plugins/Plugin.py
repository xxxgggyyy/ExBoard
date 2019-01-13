from designs import DrawerItem,DrawerContentItem

class PluginManager:

    __plugins = []

    @staticmethod
    def register(plugin):
        if isinstance(plugin, Plugin):
            PluginManager.__plugins.append(plugin)
        else:
            raise TypeError("plugin object must inherit plugin.Plugin")

#定义插件的接口
class Plugin:

    def __init__(self, name):
        self.name = name
        self.toolItems = []

    def addToolItem(self, item):
        if isinstance(item, DrawerItem):
            self.toolItems.append(item)
        else:
            raise TypeError("item must inherit DrawerItem")

    #这些定义的接口将在 Layer中相应的函数中得到调用
    def keyPressEvent(self, qkeyEvent):
        pass

    def keyReleaseEvent(self, qkeyEvent):
        pass

    def mouseDoubleClickEvent(self, qmouseEvent):
        pass

    def mouseMoveEvent(self, qmouseEvent):
        #开了Tracking所以只要鼠标移动就会调用，不用按下左键
        pass

    def mousePressEvent(self, qmouseEvent):
        pass

    def mouseReleaseEvent(self, qmouseEvent):
        pass
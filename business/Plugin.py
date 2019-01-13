#定义插件的接口
class Plugin:

    def __init__(self, name):
        self.name = name

    def init(self):#初始化代码 连接数据库 加载配置文件之类的
        '''最好不要在初始化之时调用其他插件的接口'''
        pass

    def getToolItems(self):#主程序获取插件中侧边栏的工具栏控件
        pass

    def getPluginName(self):#主程序获取插件名
        return self.name

    def getFileMenus(self, type):#主程序获取插件中需要添加到文件menu里的menu或者是action
        pass

    #这些定义的接口将在 Layer中相应的函数中得到调用
    def keyPressEvent(self, QKeyEvent):
        pass

    def keyReleaseEvent(self, QKeyEvent):
        pass

    def mouseDoubleClickEvent(self, QMouseEvent):
        pass

    def mouseMoveEvent(self, QMouseEvent):
        #开了Tracking所以只要鼠标移动就会调用，不用按下左键
        pass

    def mousePressEvent(self, QMouseEvent):
        pass

    def mouseReleaseEvent(self, QMouseEvent):
        pass

    def paintEvent(self, QPaintEvent):
        pass
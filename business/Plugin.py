from PyQt5.QtCore import QObject,pyqtSlot,pyqtSignal
#定义插件的接口
class Plugin(QObject):

    repaintSignal = pyqtSignal()

    def __init__(self, name):
        super().__init__()
        self.name = name

    def init(self):#初始化代码 连接数据库 加载配置文件之类的
        '''最好不要在初始化之时调用其他插件的接口'''
        pass

    def boardInit(self, Board):#这个初始化将会延迟到 board创建的时候才会执行
        pass

    def getToolItems(self):#主程序获取插件中侧边栏的工具栏控件
        pass

    def getPluginName(self):#主程序获取插件名
        return self.name

    def getPluginDescription(self):
        return "该插件没有描述信息"

    def getDockWidgets(self):
        pass

    def getBoardProperty(self):#返回一个 插件会给board添加的属性字符数组 主要用来在侧边栏显示
        pass

    def getFileMenus(self, type):#主程序获取插件中需要添加到文件menu里的menu或者是action
        pass

    def getPopMenus(self):
        pass

    def getPluginSettingWidget(self):
        pass

    #这些定义的接口将在 Layer中相应的函数中得到调用
    def keyPressEvent(self, QKeyEvent, Board):
        pass

    def keyReleaseEvent(self, QKeyEvent, Board):
        pass

    def mouseDoubleClickEvent(self, QMouseEvent, Board):
        pass

    def mouseMoveEvent(self, QMouseEvent, Board):
        #开了Tracking所以只要鼠标移动就会调用，不用按下左键
        pass

    def mousePressEvent(self, QMouseEvent, Board):
        pass

    def mouseReleaseEvent(self, QMouseEvent, Board):
        pass

    def paintEvent(self, QPaintEvent, Board):
        pass

    def wheelEvent(self, QWheelEvent, Board):
        pass
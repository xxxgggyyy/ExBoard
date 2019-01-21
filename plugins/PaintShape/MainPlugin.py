from business import Plugin,ExInterFace
from designs import DrawerItem, DrawerContentItem
from .PaintShapeSettingWidget import PaintShapSettingWidget
from .ExShape import *

import configparser
import copy

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QMouseEvent

class MainPlugin(Plugin):

    UNIT_MM = 0
    UNIT_CM = 1

    #定义整个插件的全局设置信息 有个默认值 实际会从配置文件读取
    unit = UNIT_MM
    unit_pixel = 3
    background_color = 'ffffff'
    font_size = 16
    line_width = 2
    conf = configparser.ConfigParser()

    conf_path = "./plugins/PaintShape/config.ini"


    #定义状态量 该状态量有一定的优先级
    FREE = 0
    PAINT_LINE = 1
    PAINT_ARC = 2
    PAINT_CIRCLE = 3

    PAINTING_LINE = 4
    PAINTING_ARC = 5
    PAINTING_CIRCLE = 6

    MOVING_LINE = 7
    MOVING_ARC = 8
    MOVING_CIRCLE = 9

    MOVING_BOARD = 10




    __state = FREE

    __painting_shape = None

    #所以有悬停对象的时候就设置这两个值 然后绘制出来
    __hover_shape = None#这个 为鼠标悬停的图形对象的一个拷贝
    __hover_point = None#这个 为悬停到的点的一个拷贝

    #匹配所有的点 是否和当前的鼠标在同x或者同y 当然，是有阈值的
    __matched_x = None
    __matched_y = None

    __shapes = []


    def __init__(self, name):
        super().__init__(name)
        self.__drawerItem = DrawerItem("绘图")
        self.__allContentItem = []#方便循环调用
        #实例化drawerContentItem
        self.__lineContenItem = DrawerContentItem("Line", parent=self.__drawerItem)
        self.__allContentItem.append(self.__lineContenItem)

        self.__arcContenItem = DrawerContentItem("Arc", parent=self.__drawerItem)
        self.__allContentItem.append(self.__arcContenItem)

        self.__circleContenItem = DrawerContentItem("Circle", parent=self.__drawerItem)
        self.__allContentItem.append(self.__circleContenItem)
        #self.__handContenItem = DrawerContentItem("Hand", parent=self.__drawerItem)
        #self.__selectContenItem = DrawerContentItem("Select", parent=self.__drawerItem)

        #添加到drawerItem
        self.__drawerItem.addContentItems(self.__allContentItem)
        #self.__drawerItem.addContentItem(self.__handContenItem)
        #self.__drawerItem.addContentItem(self.__selectContenItem)

        #连接contentItem的点击信号
        for item in self.__allContentItem:
            item.clickedSignal.connect(self.drawerItemChanged)

        self.__settingWidget = PaintShapSettingWidget(MainPlugin)

        #读取配置文件
        MainPlugin.conf.read(MainPlugin.conf_path)

        MainPlugin.background_color = MainPlugin.conf.get("setting", "background_color")
        MainPlugin.unit_pixel = MainPlugin.conf.getint("setting", "unit_pixel")
        MainPlugin.unit = MainPlugin.conf.getint("setting", "unit")
        MainPlugin.font_size = MainPlugin.conf.getint("setting", "font_size")
        MainPlugin.line_width = MainPlugin.conf.getint("setting", "line_width")

        #为widget赋值
        self.__settingWidget.ui.background_color.setText(MainPlugin.background_color)
        self.__settingWidget.ui.unit.setCurrentIndex(MainPlugin.unit)
        self.__settingWidget.ui.unit_pixel.setValue(MainPlugin.unit_pixel)
        self.__settingWidget.ui.font_size.setValue(MainPlugin.font_size)
        self.__settingWidget.ui.line_width.setValue(MainPlugin.line_width)

        #调用接口设置
        ExInterFace.setBackgroundColor(MainPlugin.background_color)

    @staticmethod
    def saveSetting():#保存到配置文件中
        try:
            MainPlugin.conf.set("setting", "background_color", str(MainPlugin.background_color))
            MainPlugin.conf.set("setting", "unit", str(MainPlugin.unit))
            MainPlugin.conf.set("setting", "unit_pixel", str(MainPlugin.unit_pixel))
            MainPlugin.conf.set("setting", "font_size", str(MainPlugin.font_size))
            MainPlugin.conf.set("setting", "line_width", str(MainPlugin.line_width))
            with open(MainPlugin.conf_path, "w") as f:
                MainPlugin.conf.write(f)
        except Exception as e:
            print(e)


    def getCurrentState(self):
        pass

    @pyqtSlot(object, bool)
    def drawerItemChanged(self, item, checked):
        if checked:
            if item is self.__lineContenItem:
                MainPlugin.__state = MainPlugin.PAINT_LINE
            elif item is self.__arcContenItem:
                MainPlugin.__state = MainPlugin.PAINT_ARC
            elif item is self.__circleContenItem:
                MainPlugin.__state = MainPlugin.PAINT_CIRCLE
            else:
                raise RuntimeError("未知错误 传入了未知的值")
        else:
            MainPlugin.__state = MainPlugin.FREE
            print("Free")

    def getToolItems(self):
        return [self.__drawerItem]

    def getPluginSettingWidget(self):
        return self.__settingWidget

    def getPluginDescription(self):
        return '''负责所有的基本的图形的绘制，添加，还有选中功能'''

    # 这些定义的接口将在 Board中相应的函数中得到调用
    def keyPressEvent(self, QKeyEvent, Board):
        if MainPlugin.__state == MainPlugin.PAINT_LINE:
            pass
        elif MainPlugin.__state == MainPlugin.PAINT_CIRCLE:
            pass
        elif MainPlugin.__state == MainPlugin.PAINT_ARC:
            pass
        elif MainPlugin.__state == MainPlugin.PAINTING_ARC:
            pass
        elif MainPlugin.__state == MainPlugin.PAINTING_CIRCLE:
            pass
        elif MainPlugin.__state == MainPlugin.PAINTING_LINE:
            pass
        elif MainPlugin.__state == MainPlugin.FREE:
            pass
        elif MainPlugin.__state == MainPlugin.MOVING_ARC:
            pass
        elif MainPlugin.__state == MainPlugin.MOVING_LINE:
            pass
        elif MainPlugin.__state == MainPlugin.MOVING_CIRCLE:
            pass
        elif MainPlugin.__state == MainPlugin.MOVING_BOARD:
            pass

    def keyReleaseEvent(self, QKeyEvent, Board):
        if MainPlugin.__state == MainPlugin.PAINT_LINE:
            pass
        elif MainPlugin.__state == MainPlugin.PAINT_CIRCLE:
            pass
        elif MainPlugin.__state == MainPlugin.PAINT_ARC:
            pass
        elif MainPlugin.__state == MainPlugin.PAINTING_ARC:
            pass
        elif MainPlugin.__state == MainPlugin.PAINTING_CIRCLE:
            pass
        elif MainPlugin.__state == MainPlugin.PAINTING_LINE:
            pass
        elif MainPlugin.__state == MainPlugin.FREE:
            pass
        elif MainPlugin.__state == MainPlugin.MOVING_ARC:
            pass
        elif MainPlugin.__state == MainPlugin.MOVING_LINE:
            pass
        elif MainPlugin.__state == MainPlugin.MOVING_CIRCLE:
            pass
        elif MainPlugin.__state == MainPlugin.MOVING_BOARD:
            pass

    def mouseDoubleClickEvent(self, QMouseEvent, Board):
        if MainPlugin.__state == MainPlugin.PAINT_LINE:
            pass
        elif MainPlugin.__state == MainPlugin.PAINT_CIRCLE:
            pass
        elif MainPlugin.__state == MainPlugin.PAINT_ARC:
            pass
        elif MainPlugin.__state == MainPlugin.PAINTING_ARC:
            pass
        elif MainPlugin.__state == MainPlugin.PAINTING_CIRCLE:
            pass
        elif MainPlugin.__state == MainPlugin.PAINTING_LINE:
            pass
        elif MainPlugin.__state == MainPlugin.FREE:
            pass
        elif MainPlugin.__state == MainPlugin.MOVING_ARC:
            pass
        elif MainPlugin.__state == MainPlugin.MOVING_LINE:
            pass
        elif MainPlugin.__state == MainPlugin.MOVING_CIRCLE:
            pass
        elif MainPlugin.__state == MainPlugin.MOVING_BOARD:
            pass

    def mouseMoveEvent(self, QMouseEvent, Board):
        mousePos = MainPlugin.translatePt(ExPoint(QMouseEvent.pos()), Board)
        # 开了Tracking所以只要鼠标移动就会调用，不用按下左键

        # 检查 并设置悬停
        if not self.checkHover(mousePos):
            self.checkMatch(mousePos)

        if MainPlugin.__state == MainPlugin.PAINT_LINE:
            pass
        elif MainPlugin.__state == MainPlugin.PAINT_CIRCLE:
            pass
        elif MainPlugin.__state == MainPlugin.PAINT_ARC:
            pass
        elif MainPlugin.__state == MainPlugin.PAINTING_ARC:
            pass
        elif MainPlugin.__state == MainPlugin.PAINTING_CIRCLE:
            pass
        elif MainPlugin.__state == MainPlugin.PAINTING_LINE:
            matchedPt = self.getMatchedPoint(mousePos)
            MainPlugin.__painting_shape.setPt1(matchedPt.x, matchedPt.y)
        elif MainPlugin.__state == MainPlugin.FREE:
            pass
        elif MainPlugin.__state == MainPlugin.MOVING_ARC:
            pass
        elif MainPlugin.__state == MainPlugin.MOVING_LINE:
            pass
        elif MainPlugin.__state == MainPlugin.MOVING_CIRCLE:
            pass
        elif MainPlugin.__state == MainPlugin.MOVING_BOARD:
            pass

        Board.repaint()

    def mousePressEvent(self, QMouseEvent, Board):
        if MainPlugin.__state == MainPlugin.PAINT_LINE:
            pass
        elif MainPlugin.__state == MainPlugin.PAINT_CIRCLE:
            pass
        elif MainPlugin.__state == MainPlugin.PAINT_ARC:
            pass
        elif MainPlugin.__state == MainPlugin.PAINTING_ARC:
            pass
        elif MainPlugin.__state == MainPlugin.PAINTING_CIRCLE:
            pass
        elif MainPlugin.__state == MainPlugin.PAINTING_LINE:
            pass
        elif MainPlugin.__state == MainPlugin.FREE:
            pass
        elif MainPlugin.__state == MainPlugin.MOVING_ARC:
            pass
        elif MainPlugin.__state == MainPlugin.MOVING_LINE:
            pass
        elif MainPlugin.__state == MainPlugin.MOVING_CIRCLE:
            pass
        elif MainPlugin.__state == MainPlugin.MOVING_BOARD:
            pass

    def mouseReleaseEvent(self, QMouseEvent, Board):

        # 坐标转换 将鼠标坐标转换为 常用数学坐标
        mousePos = MainPlugin.translatePt(ExPoint(QMouseEvent.pos()), Board)

        if MainPlugin.__state == MainPlugin.PAINT_LINE:
            matchedPt = self.getMatchedPoint(mousePos)
            MainPlugin.__painting_shape = ExLine(matchedPt.x, matchedPt.y, mousePos.x, mousePos.y)
            MainPlugin.__state = MainPlugin.PAINTING_LINE
        elif MainPlugin.__state == MainPlugin.PAINT_CIRCLE:
            pass
        elif MainPlugin.__state == MainPlugin.PAINT_ARC:
            pass
        elif MainPlugin.__state == MainPlugin.PAINTING_ARC:
            pass
        elif MainPlugin.__state == MainPlugin.PAINTING_CIRCLE:
            pass
        elif MainPlugin.__state == MainPlugin.PAINTING_LINE:
            MainPlugin.__state = MainPlugin.PAINT_LINE
            MainPlugin.__shapes.append(MainPlugin.__painting_shape)
            MainPlugin.__painting_shape = None
        elif MainPlugin.__state == MainPlugin.FREE:
            pass
        elif MainPlugin.__state == MainPlugin.MOVING_ARC:
            pass
        elif MainPlugin.__state == MainPlugin.MOVING_LINE:
            pass
        elif MainPlugin.__state == MainPlugin.MOVING_CIRCLE:
            pass
        elif MainPlugin.__state == MainPlugin.MOVING_BOARD:
            pass

    @staticmethod
    def translatePt(pt, Board):#从实际坐标 转换成qt默认坐标系的位置
        re = ExPoint(0, 0)
        re.x = pt.x / MainPlugin.unit_pixel
        re.y = (Board.height() - pt.y) / MainPlugin.unit_pixel
        return re

    def checkHover(self, mousePt):
        #遍历所有的对象和点 判断时候鼠标悬停在图形上
        #先遍历点
        allPoints = []
        #生成所有的点列表
        for shape in MainPlugin.__shapes:
            allPoints += shape.getPoints()
        #检查是否悬停到点上了
        for pt in allPoints:
            if pt.isPointNearShape(mousePt, 2.5, MainPlugin):
                MainPlugin.__hover_point = CirclePoint(pt)
                MainPlugin.__hover_shape = None
                return True
        #没有检测到 设置为None
        MainPlugin.__hover_point = None

        #然后检查所有的图形
        if MainPlugin.__state <= MainPlugin.PAINT_CIRCLE:#在没有绘制图形的时候 才有hover直线的效果
            for shape in MainPlugin.__shapes:
                if shape.isPointOnShape(mousePt, MainPlugin):
                    MainPlugin.__hover_shape = copy.deepcopy(shape)
                    MainPlugin.__hover_shape.setColor(Qt.green)
                    return True
        MainPlugin.__hover_shape = None

        return False

    def checkMatch(self, mousePt):
        threshold = 2.1
        allPoints = []
        # 生成所有的点列表
        for shape in MainPlugin.__shapes:
            allPoints += shape.getPoints()

        if MainPlugin.__painting_shape:#在把正在绘制的线的初始点给加上
            if isinstance(MainPlugin.__painting_shape, ExLine):
                allPoints.append(MainPlugin.__painting_shape.pt0)

        matchedX = False
        matchedY = False

        for pt in allPoints:
            if mousePt.x < pt.x+threshold and mousePt.x > pt.x-threshold:
                MainPlugin.__matched_x = pt.x
                matchedX = True
            if mousePt.y < pt.y + threshold and mousePt.y > pt.y - threshold:
                MainPlugin.__matched_y = pt.y
                matchedY = True

        if not matchedX:
            MainPlugin.__matched_x = None

        if not matchedY:
            MainPlugin.__matched_y = None

        if matchedX or matchedY:
            return True
        else:
            return False

    def getMatchedPoint(self, mousePt):#其实就是综合了 hover的点 和matchedX,y 得到点
        x = mousePt.x
        y = mousePt.y
        if MainPlugin.__hover_point:
            x = MainPlugin.__hover_point.x
            y = MainPlugin.__hover_point.y
        else:
            # 没有hover到点就设置成匹配到的x,y
            if MainPlugin.__matched_y:
                y = MainPlugin.__matched_y
            if MainPlugin.__matched_x:
                x = MainPlugin.__matched_x

        return ExPoint(x,y)


    def paintEvent(self, QPaintEvent, Board):
        painter = QPainter(Board)
        painter.setRenderHint(QPainter.Antialiasing, True)#打开反走样
        #在坐标转换之前先绘制文字

        #坐标系转换为 x朝上和y朝右的通用数学坐标系
        painter.setWindow(0, Board.height(), Board.width(), -Board.height())

        #绘制图形
        for shape in MainPlugin.__shapes:
            shape.draw(painter, MainPlugin)

        #绘制正在绘制的图形
        if MainPlugin.__painting_shape:
            MainPlugin.__painting_shape.draw(painter, MainPlugin)

        #绘制悬停对象
        if MainPlugin.__hover_point:
            MainPlugin.__hover_point.draw(painter, MainPlugin)

        if MainPlugin.__hover_shape:
            MainPlugin.__hover_shape.draw(painter, MainPlugin)

        #绘制 匹配到的虚线
        vLine = None
        hLine = None
        if MainPlugin.__matched_x:
            vLine = FreeLine(MainPlugin.__matched_x,0,MainPlugin.__matched_x,Board.height())
        if MainPlugin.__matched_y:
            hLine = FreeLine(0,MainPlugin.__matched_y,Board.width(),MainPlugin.__matched_y)
        if vLine:
            vLine.draw(painter, MainPlugin)
        if hLine:
            hLine.draw(painter, MainPlugin)


        if MainPlugin.__state == MainPlugin.PAINT_LINE:
            pass
        elif MainPlugin.__state == MainPlugin.PAINT_CIRCLE:
            pass
        elif MainPlugin.__state == MainPlugin.PAINT_ARC:
            pass
        elif MainPlugin.__state == MainPlugin.PAINTING_ARC:
            pass
        elif MainPlugin.__state == MainPlugin.PAINTING_CIRCLE:
            pass
        elif MainPlugin.__state == MainPlugin.PAINTING_LINE:
            pass
        elif MainPlugin.__state == MainPlugin.FREE:
            pass
        elif MainPlugin.__state == MainPlugin.MOVING_ARC:
            pass
        elif MainPlugin.__state == MainPlugin.MOVING_LINE:
            pass
        elif MainPlugin.__state == MainPlugin.MOVING_CIRCLE:
            pass
        elif MainPlugin.__state == MainPlugin.MOVING_BOARD:
            pass
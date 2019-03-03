from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMenu,QAction
from PyQt5.QtGui import QMouseEvent

from .designs import resources

from business import Plugin,ExInterFace
from designs import DrawerItem, DrawerContentItem
from .PaintShapeSettingWidget import PaintShapSettingWidget
from .ExShape import *
from .ShapePropertyDockWidget import ShapePropertyDockWidget

import configparser
import copy
import math

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
    PAINTING_ARC0 = 5
    PAINTING_ARC1 = 6
    PAINTING_CIRCLE = 7

    MOVING_SHAPE = 8

    SELECT = 9
    HAND = 10
    HANDED = 11



    MOVING_BOARD = 12

    __origin_position = {}#原点坐标

    __scale = {}#缩放

    __state = {}

    __painting_shape = {}

    #所以有悬停对象的时候就设置这两个值 然后绘制出来
    __hover_shape = {}#这个 为鼠标悬停的图形对象的一个拷贝
    __hover_point = {}#这个 为悬停到的点的一个拷贝

    #匹配所有的点 是否和当前的鼠标在同x或者同y 当然，是有阈值的
    __matched_x = {}
    __matched_y = {}

    __shapes = {}

    __assist_circle = {}#PAINT_CIRCLE时的虚线圆

    __assist_line = {}#绘制圆弧时的辅助虚线

    __hand_start_pt = {}#hand按下时的点

    __changing_pt = {}

    __origin_cross = ExOriginCross()


    def __init__(self, name):
        super().__init__(name)
        self.__drawerItem = DrawerItem("绘图")
        self.__allContentItem = []#方便循环调用


        #实例化drawerContentItem 即用于侧边栏的按钮
        self.__lineContenItem = DrawerContentItem("直线(&Q)", parent=self.__drawerItem, icon=QIcon(":/paintshape_res/img/line.png"))
        self.__allContentItem.append(self.__lineContenItem)

        self.__arcContenItem = DrawerContentItem("圆弧(&W)", parent=self.__drawerItem, icon=QIcon(":/paintshape_res/img/arc.png"))
        self.__allContentItem.append(self.__arcContenItem)

        self.__circleContenItem = DrawerContentItem("圆(&E)", parent=self.__drawerItem, icon=QIcon(":/paintshape_res/img/circle.png"))
        self.__allContentItem.append(self.__circleContenItem)

        self.__handContenItem = DrawerContentItem("Hand(&R)", parent=self.__drawerItem, icon=QIcon(":/paintshape_res/img/hand.png"))
        self.__allContentItem.append(self.__handContenItem)

        self.__selectContenItem = DrawerContentItem("选择(&T)", parent=self.__drawerItem, icon=QIcon(":/paintshape_res/img/select.png"))
        self.__allContentItem.append(self.__selectContenItem)

        #添加到drawerItem
        self.__drawerItem.addContentItems(self.__allContentItem)

        #创建属性dockwidget
        self.propertyDock = ShapePropertyDockWidget("图形属性")
        self.propertyDock.setMinimumWidth(300)

        #菜单
        self.paintShapeMenu = QMenu("绘图")

        self.lineAction = QAction(QIcon(":/paintshape_res/img/line.png"), "直线(&Q)", self.paintShapeMenu)#讲道理 这里可以用eval简化写法
        self.lineAction.setCheckable(True)
        self.lineAction.triggered.connect(self.lineActionToggled)
        self.paintShapeMenu.addAction(self.lineAction)

        self.arcAction = QAction(QIcon(":/paintshape_res/img/arc.png"), "圆弧(&W)", self.paintShapeMenu)
        self.arcAction.setCheckable(True)
        self.arcAction.triggered.connect(self.arcActionToggled)
        self.paintShapeMenu.addAction(self.arcAction)

        self.circleAction = QAction(QIcon(":/paintshape_res/img/circle.png"), "圆(&E)", self.paintShapeMenu)
        self.circleAction.setCheckable(True)
        self.circleAction.triggered.connect(self.circleActionToggled)
        self.paintShapeMenu.addAction(self.circleAction)

        self.handAction = QAction(QIcon(":/paintshape_res/img/hand.png"), "Hand(&R)", self.paintShapeMenu)
        self.handAction.setCheckable(True)
        self.handAction.triggered.connect(self.handActionToggled)
        self.paintShapeMenu.addAction(self.handAction)

        self.selectAction = QAction(QIcon(":/paintshape_res/img/select.png"), "选择(&T)", self.paintShapeMenu)
        self.selectAction.setCheckable(True)
        self.selectAction.triggered.connect(self.selectActionToggled)
        self.paintShapeMenu.addAction(self.selectAction)

        self.deleteAction = QAction(QIcon(":/paintshape_res/img/delete.png"),"删除选中(&Delete)",self.paintShapeMenu)
        self.deleteAction.triggered.connect(self.deleteActionTrigger)
        self.paintShapeMenu.addAction(self.deleteAction)

        self.revokeAction = QAction(QIcon(":/paintshape_res/img/revoke.png"), "撤销(ctr+Z)", self.paintShapeMenu)
        self.revokeAction.triggered.connect(self.revokeActionTrigger)
        self.paintShapeMenu.addAction(self.revokeAction)

        self.forwardAction = QAction(QIcon(":/paintshape_res/img/forward.png"), "前进(ctr+X)", self.paintShapeMenu)
        self.forwardAction.triggered.connect(self.forwardActionTrigger)
        self.paintShapeMenu.addAction(self.forwardAction)

        self.showPropertyDockAction = QAction(QIcon(":/paintshape_res/img/show.png"), "显示属性窗口", self.paintShapeMenu)
        self.showPropertyDockAction.triggered.connect(self.propertyDock.show)
        self.paintShapeMenu.addAction(self.showPropertyDockAction)

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

    def getTopToolBarActions(self):
        return [self.revokeAction, self.forwardAction]

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
            raise e

    def getDockWidgets(self):
        return [self.propertyDock]

    def getCurrentSelectedState(self):
        for item in self.__allContentItem:
            if item.isChecked():
                if item is self.__lineContenItem:
                    return MainPlugin.PAINT_LINE
                elif item is self.__arcContenItem:
                    return MainPlugin.PAINT_ARC
                elif item is self.__circleContenItem:
                    return MainPlugin.PAINT_CIRCLE
                elif item is self.__selectContenItem:
                    return MainPlugin.SELECT
                elif item is self.__handContenItem:
                    return MainPlugin.HAND

        return MainPlugin.FREE

    @pyqtSlot(bool)
    def lineActionToggled(self, b):
        if b:
            for action in self.paintShapeMenu.actions():
                action.setChecked(False)
            self.lineAction.setChecked(True)
        self.__drawerItem.setChecked(self.__lineContenItem,b)

    @pyqtSlot(bool)
    def arcActionToggled(self, b):
        if b:
            for action in self.paintShapeMenu.actions():
                action.setChecked(False)
            self.arcAction.setChecked(True)
        self.__drawerItem.setChecked(self.__arcContenItem, b)

    @pyqtSlot(bool)
    def circleActionToggled(self, b):
        if b:
            for action in self.paintShapeMenu.actions():
                action.setChecked(False)
            self.circleAction.setChecked(True)
        self.__drawerItem.setChecked(self.__circleContenItem, b)

    @pyqtSlot(bool)
    def handActionToggled(self, b):
        if b:
            for action in self.paintShapeMenu.actions():
                action.setChecked(False)
            self.handAction.setChecked(True)
        self.__drawerItem.setChecked(self.__handContenItem, b)

    @pyqtSlot(bool)
    def selectActionToggled(self, b):
        if b:
            for action in self.paintShapeMenu.actions():
                action.setChecked(False)
            self.selectAction.setChecked(True)
        self.__drawerItem.setChecked(self.__selectContenItem, b)

    @pyqtSlot(bool)
    def deleteActionTrigger(self):
        #self.__drawerItem.setChecked(self.__selectContenItem, b)
        Board = ExInterFace.getCurrentBoard()
        for i in range(len(MainPlugin.__shapes[Board.id])-1, -1, -1):
            if MainPlugin.__shapes[Board.id][i].selected:
                MainPlugin.__shapes[Board.id].pop(i)
        Board.repaint()

    @pyqtSlot(bool)
    def revokeActionTrigger(self):
        pass

    @pyqtSlot(bool)
    def forwardActionTrigger(self):
        pass

    @pyqtSlot(object, bool)
    def drawerItemChanged(self, item, checked):
        self.clearCurrentVar()
        Board = ExInterFace.getCurrentBoard()
        for action in self.paintShapeMenu.actions():
            action.setChecked(False)
        if checked:
            if item is self.__lineContenItem:
                MainPlugin.__state[Board.id] = MainPlugin.PAINT_LINE
                self.lineAction.setChecked(True)
            elif item is self.__arcContenItem:
                MainPlugin.__state[Board.id] = MainPlugin.PAINT_ARC
                self.arcAction.setChecked(True)
            elif item is self.__circleContenItem:
                MainPlugin.__state[Board.id] = MainPlugin.PAINT_CIRCLE
                self.circleAction.setChecked(True)
            elif item is self.__selectContenItem:
                MainPlugin.__state[Board.id] = MainPlugin.SELECT
                self.selectAction.setChecked(True)
            elif item is self.__handContenItem:
                MainPlugin.__state[Board.id] = MainPlugin.HAND
                self.handAction.setChecked(True)
            else:
                raise RuntimeError("未知错误 传入了未知的值")
        else:
            MainPlugin.__state[Board.id] = MainPlugin.FREE

        Board.repaint()

    def getToolItems(self):
        return [self.__drawerItem]

    def getPluginSettingWidget(self):
        return self.__settingWidget

    def getPluginDescription(self):
        return '''负责所有的基本的图形的绘制，添加，还有选中功能'''

    # 这些定义的接口将在 Board中相应的函数中得到调用
    def keyPressEvent(self, QKeyEvent):
        Board = ExInterFace.getCurrentBoard()

        key_value = QKeyEvent.key()

        if key_value == Qt.Key_Q:
            self.__drawerItem.setChecked(self.__lineContenItem, True)
        elif key_value == Qt.Key_W:
            self.__drawerItem.setChecked(self.__arcContenItem, True)
        elif key_value == Qt.Key_E:
            self.__drawerItem.setChecked(self.__circleContenItem, True)
        elif key_value == Qt.Key_R:
            self.__drawerItem.setChecked(self.__handContenItem, True)
        elif key_value == Qt.Key_T:
            self.__drawerItem.setChecked(self.__selectContenItem, True)
        elif key_value == Qt.Key_Escape:
            if MainPlugin.__state[Board.id] == MainPlugin.PAINTING_ARC0 or MainPlugin.__state[Board.id] == MainPlugin.PAINTING_ARC1:
                MainPlugin.__state[Board.id] = MainPlugin.PAINT_ARC
            elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_CIRCLE:
                MainPlugin.__state[Board.id] = MainPlugin.PAINT_CIRCLE
                MainPlugin.__assist_circle[Board.id].setVisible(True)
            elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_LINE:
                MainPlugin.__state[Board.id] = MainPlugin.PAINT_LINE
        elif key_value == Qt.Key_Delete:
            self.deleteActionTrigger()

        if MainPlugin.__state[Board.id] == MainPlugin.PAINT_LINE:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINT_CIRCLE:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINT_ARC:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_ARC0:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_CIRCLE:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_LINE:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.FREE:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.MOVING_BOARD:
            pass

        Board.repaint()

    def keyReleaseEvent(self, QKeyEvent):
        Board = ExInterFace.getCurrentBoard()
        if MainPlugin.__state[Board.id] == MainPlugin.PAINT_LINE:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINT_CIRCLE:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINT_ARC:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_ARC0:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_CIRCLE:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_LINE:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.FREE:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.MOVING_BOARD:
            pass

    def getMenu(self):
        return self.paintShapeMenu


    def mouseDoubleClickEvent(self, QMouseEvent):
        Board = ExInterFace.getCurrentBoard()
        if MainPlugin.__state[Board.id] == MainPlugin.PAINT_LINE:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINT_CIRCLE:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINT_ARC:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_ARC0:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_CIRCLE:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_LINE:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.FREE:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.MOVING_BOARD:
            pass

    def mouseMoveEvent(self, QMouseEvent):
        Board = ExInterFace.getCurrentBoard()
        mousePos = MainPlugin.translatePt(QMouseEvent.pos(), Board)

        # 开了Tracking所以只要鼠标移动就会调用，不用按下左键

        # 检查 并设置悬停

        # 只有在选中模式下 才有shape的hover
        if MainPlugin.__state[Board.id] == MainPlugin.SELECT:
            self.checkHoverShape(mousePos, Board)

        #在绘制，绘制中，选中 都可以有 hover点和匹配
        # 原则是点到点 就不会点到shape
        if MainPlugin.__state[Board.id] < MainPlugin.SELECT:
            self.checkHoverPoint(mousePos, Board)
            self.checkMatch(mousePos, Board)

        #一定要在上面代码的后面
        matchedPt = self.getMatchedPoint(mousePos, Board)

        if MainPlugin.__state[Board.id] == MainPlugin.PAINT_LINE:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINT_CIRCLE:
            if not MainPlugin.__assist_circle[Board.id]:
                MainPlugin.__assist_circle[Board.id] = ExCircle(matchedPt, 10)
                MainPlugin.__assist_circle[Board.id].setPenStyle(Qt.DotLine)
            MainPlugin.__assist_circle[Board.id].centerPt = matchedPt
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINT_ARC:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_ARC0:
            if MainPlugin.__assist_line[Board.id]:
                MainPlugin.__assist_line[Board.id].setPt1(matchedPt)
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_ARC1:
            if MainPlugin.__painting_shape[Board.id]:
                if not matchedPt == MainPlugin.__painting_shape[Board.id].pt0 and not matchedPt == MainPlugin.__painting_shape[Board.id].pt1:
                    #MainPlugin.__painting_shape
                    MainPlugin.__painting_shape[Board.id].setPt2(matchedPt)
                    if not MainPlugin.__painting_shape[Board.id].calculate():
                        MainPlugin.__painting_shape[Board.id].setVisible(False)
                    else:
                        MainPlugin.__painting_shape[Board.id].setVisible(True)
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_CIRCLE:
            if MainPlugin.__painting_shape[Board.id]:
                #计算半径
                r = math.sqrt((matchedPt.x - MainPlugin.__painting_shape[Board.id].centerPt.x)**2 + (matchedPt.y - MainPlugin.__painting_shape[Board.id].centerPt.y)**2)
                MainPlugin.__painting_shape[Board.id].r = r
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_LINE:
            if MainPlugin.__painting_shape[Board.id]:
                #matchedPt = self.getMatchedPoint(mousePos, Board)
                MainPlugin.__painting_shape[Board.id].setPt1(matchedPt.x, matchedPt.y)
        elif MainPlugin.__state[Board.id] == MainPlugin.FREE:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.MOVING_BOARD:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.HANDED:
            MainPlugin.__origin_position[Board.id].x += (QMouseEvent.pos().x() - MainPlugin.__hand_start_pt[Board.id].x)/ MainPlugin.unit_pixel
            MainPlugin.__origin_position[Board.id].y -= (QMouseEvent.pos().y() - MainPlugin.__hand_start_pt[Board.id].y)/ MainPlugin.unit_pixel
            MainPlugin.__hand_start_pt[Board.id].x = QMouseEvent.pos().x()
            MainPlugin.__hand_start_pt[Board.id].y = QMouseEvent.pos().y()
        elif MainPlugin.__state[Board.id] == MainPlugin.MOVING_SHAPE:
            #直接修改 hover_pt的值
            MainPlugin.__changing_pt[Board.id].x = matchedPt.x
            MainPlugin.__changing_pt[Board.id].y = matchedPt.y

            if not MainPlugin.__changing_pt[Board.id].parent.calculate():#需要间接计算一下
                MainPlugin.__changing_pt[Board.id].parent.setVisible(False)
            else:
                MainPlugin.__changing_pt[Board.id].parent.setVisible(True)

        Board.repaint()

    def mousePressEvent(self, QMouseEvent):
        Board = ExInterFace.getCurrentBoard()
        # 坐标转换 将鼠标坐标转换为 常用数学坐标
        mousePos = MainPlugin.translatePt(QMouseEvent.pos(), Board)
        if QMouseEvent.button() == Qt.LeftButton:
            if MainPlugin.__state[Board.id] == MainPlugin.PAINT_LINE:
                pass
            elif MainPlugin.__state[Board.id] == MainPlugin.PAINT_CIRCLE:
                pass
            elif MainPlugin.__state[Board.id] == MainPlugin.PAINT_ARC:
                pass
            elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_ARC0:
                pass
            elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_ARC1:
                pass
            elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_CIRCLE:
                pass
            elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_LINE:
                pass
            elif MainPlugin.__state[Board.id] == MainPlugin.FREE:
                pass
            elif MainPlugin.__state[Board.id] == MainPlugin.MOVING_BOARD:
                pass
            elif MainPlugin.__state[Board.id] == MainPlugin.HAND:
                #if not MainPlugin.__hand_start_pt[Board.id]:
                    #MainPlugin.__hand_start_pt[Board.id] = ExPoint(mousePos)
                MainPlugin.__hand_start_pt[Board.id].x = QMouseEvent.pos().x()#这里使用Boadr坐标没有转换后的，移动就必须要一个原点固定的坐标系
                MainPlugin.__hand_start_pt[Board.id].y = QMouseEvent.pos().y()
                MainPlugin.__state[Board.id] = MainPlugin.HANDED
            elif MainPlugin.__state[Board.id] == MainPlugin.SELECT:
                pt = self.getPressPoint(mousePos)#查找是否点击到点上
                selectedShapes = self.getSelectShapes()
                if pt and len(selectedShapes)==1 and pt.parent == selectedShapes[0]:
                    # 如果点到了点且是当前选中的点 就开始准备移动
                    MainPlugin.__state[Board.id] = MainPlugin.MOVING_SHAPE
                    MainPlugin.__changing_pt[Board.id] = pt
                else:
                    if not QMouseEvent.modifiers() == Qt.ControlModifier:#没有按下ctr 清空所有的选择
                        self.cancelAllSelected()
                    if MainPlugin.__hover_shape[Board.id]:#有点到 图形上
                        MainPlugin.__hover_shape[Board.id].origin_shape.selected = True
                        self.propertyDock.updateValues(MainPlugin.__hover_shape[Board.id].origin_shape)
                    else:
                        self.propertyDock.clearAll()
                    

        Board.repaint()

    def mouseReleaseEvent(self, QMouseEvent):

        Board = ExInterFace.getCurrentBoard()

        # 坐标转换 将鼠标坐标转换为 常用数学坐标
        mousePos = MainPlugin.translatePt(QMouseEvent.pos(), Board)

        matchedPt = self.getMatchedPoint(mousePos, Board)

        if QMouseEvent.button() == Qt.LeftButton:
            if MainPlugin.__state[Board.id] == MainPlugin.PAINT_LINE:
                #matchedPt = self.getMatchedPoint(mousePos, Board)
                MainPlugin.__painting_shape[Board.id] = ExLine(matchedPt.x, matchedPt.y, mousePos.x, mousePos.y)
                MainPlugin.__state[Board.id] = MainPlugin.PAINTING_LINE
            elif MainPlugin.__state[Board.id] == MainPlugin.PAINT_CIRCLE:
                MainPlugin.__painting_shape[Board.id] = ExCircle(matchedPt.x,matchedPt.y,0)
                MainPlugin.__assist_circle[Board.id].setVisible(False)
                MainPlugin.__state[Board.id] = MainPlugin.PAINTING_CIRCLE
            elif MainPlugin.__state[Board.id] == MainPlugin.PAINT_ARC:
                MainPlugin.__painting_shape[Board.id] = ExArc()
                MainPlugin.__assist_line[Board.id] = ExLine()
                MainPlugin.__assist_line[Board.id].setPenStyle(Qt.DotLine)
                MainPlugin.__painting_shape[Board.id].setPt0(matchedPt)
                MainPlugin.__assist_line[Board.id].setPt0(matchedPt)
                MainPlugin.__state[Board.id] = MainPlugin.PAINTING_ARC0
            elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_ARC0:
                if matchedPt != MainPlugin.__painting_shape[Board.id].pt0:
                    MainPlugin.__state[Board.id] = MainPlugin.PAINTING_ARC1
                    MainPlugin.__painting_shape[Board.id].setPt1(matchedPt)
                    MainPlugin.__assist_line[Board.id].setPt1(matchedPt)
            elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_ARC1:
                if MainPlugin.__painting_shape[Board.id].isVisible() and not matchedPt == MainPlugin.__painting_shape[Board.id].pt0 and not matchedPt == MainPlugin.__painting_shape[Board.id].pt1:
                    MainPlugin.__state[Board.id] = MainPlugin.PAINT_ARC
                    MainPlugin.__painting_shape[Board.id].setPt2(matchedPt)
                    MainPlugin.__shapes[Board.id].append(MainPlugin.__painting_shape[Board.id])
                    MainPlugin.__painting_shape[Board.id] = None
                    MainPlugin.__assist_line[Board.id] = None
            elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_CIRCLE:
                if MainPlugin.__painting_shape[Board.id]:
                    MainPlugin.__shapes[Board.id].append(MainPlugin.__painting_shape[Board.id])
                    MainPlugin.__assist_circle[Board.id].setVisible(True)
                    MainPlugin.__assist_circle[Board.id].centerPt = matchedPt
                MainPlugin.__state[Board.id] = MainPlugin.PAINT_CIRCLE

            elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_LINE:
                if MainPlugin.__painting_shape[Board.id]:
                    MainPlugin.__shapes[Board.id].append(MainPlugin.__painting_shape[Board.id])
                    MainPlugin.__painting_shape[Board.id] = None
                MainPlugin.__state[Board.id] = MainPlugin.PAINT_LINE
            elif MainPlugin.__state[Board.id] == MainPlugin.FREE:
                pass
            elif MainPlugin.__state[Board.id] == MainPlugin.MOVING_BOARD:
                pass
            elif MainPlugin.__state[Board.id] == MainPlugin.SELECT:
                pass
            elif MainPlugin.__state[Board.id] == MainPlugin.HANDED:
                MainPlugin.__state[Board.id] = MainPlugin.HAND
            elif MainPlugin.__state[Board.id] == MainPlugin.MOVING_SHAPE:
                MainPlugin.__state[Board.id] = MainPlugin.SELECT#鼠标松开 返回到选择状态
                MainPlugin.__hover_shape[Board.id] = None
        elif QMouseEvent.button() == Qt.RightButton:
            if MainPlugin.__state[Board.id] == MainPlugin.PAINT_LINE:
                pass
            elif MainPlugin.__state[Board.id] == MainPlugin.PAINT_CIRCLE:
                pass
            elif MainPlugin.__state[Board.id] == MainPlugin.PAINT_ARC:
                pass
            elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_ARC0:
                pass
            elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_CIRCLE:
                pass
            elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_LINE:
                pass
            elif MainPlugin.__state[Board.id] == MainPlugin.FREE:
                pass
            elif MainPlugin.__state[Board.id] == MainPlugin.MOVING_BOARD:
                pass
            elif MainPlugin.__state[Board.id] == MainPlugin.SELECT:
                pass

        Board.repaint()

    def cancelAllSelected(self):
        Board = ExInterFace.getCurrentBoard()
        for shape in MainPlugin.__shapes[Board.id]:
            shape.selected = False

    def wheelEvent(self, QWheelEvent):

        Board = ExInterFace.getCurrentBoard()

        if MainPlugin.__state[Board.id] != MainPlugin.FREE:
            # 根据鼠标滚轮缩放
            if QWheelEvent.angleDelta().y() > 0:
                MainPlugin.__scale[Board.id] += 0.03
            else:
                MainPlugin.__scale[Board.id] -= 0.03
            Board.repaint()
        
        if MainPlugin.__state[Board.id] == MainPlugin.PAINT_LINE:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINT_CIRCLE:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINT_ARC:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_ARC0:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_CIRCLE:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_LINE:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.FREE:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.MOVING_BOARD:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.SELECT:
            pass


    @staticmethod
    def translatePt(pt, Board):#从实际坐标 转换成qt默认坐标系的位置
        re = ExPoint(0, 0)
        re.x = pt.x() / MainPlugin.unit_pixel
        re.y = (Board.height() - pt.y()) / MainPlugin.unit_pixel

        #代入origin_pt的计算偏移量
        re.x -= MainPlugin.__origin_position[Board.id].x
        re.y -= MainPlugin.__origin_position[Board.id].y

        #代入scale计算偏移
        re.x /= MainPlugin.__scale[Board.id]
        re.y /= MainPlugin.__scale[Board.id]
        return re

    def getPressPoint(self, mousePt):#主要是用于获取 点击的点 来拉动修改图形 为了和checkHoverPoint解耦
        allPoints = []
        Board = ExInterFace.getCurrentBoard()
        # 生成所有的点列表
        for shape in MainPlugin.__shapes[Board.id]:
            allPoints += shape.getPoints()
        # 检查是否悬停到点上了
        for pt in allPoints:
            if pt.isPointNearShape(mousePt, 2.5, MainPlugin) and pt.parent.selected:
                return pt
        return None

    def getSelectShapes(self):
        Board = ExInterFace.getCurrentBoard()
        result = []
        for shape in MainPlugin.__shapes[Board.id]:
            if shape.selected:
                result.append(shape)
        return result

    def checkHoverPoint(self, mousePt, Board):
        allPoints = []
        # 生成所有的点列表
        for shape in MainPlugin.__shapes[Board.id]:
            allPoints += shape.getPoints()
        if MainPlugin.__state[Board.id] == MainPlugin.MOVING_SHAPE:
            allPoints.remove(MainPlugin.__changing_pt[Board.id])#在移动的时候自身 就不要匹配了 这里很耦合 之后优化的时候应该考虑解耦
        # 检查是否悬停到点上了
        for pt in allPoints:
            if pt.isPointNearShape(mousePt, 2.5, MainPlugin):
                MainPlugin.__hover_point[Board.id] = CirclePoint(pt)
                #MainPlugin.__hover_point[Board.id].orgpt = pt  # 将这个point设置一下 方便一会儿的拖动修改图形
                MainPlugin.__hover_shape[Board.id] = None
                return True
        # 没有检测到 设置为None
        MainPlugin.__hover_point[Board.id] = None
        return False

    def checkHoverShape(self, mousePt, Board):

        # 然后检查所有的图形
        for shape in MainPlugin.__shapes[Board.id]:
            if shape.isPointOnShape(mousePt, MainPlugin):
                MainPlugin.__hover_shape[Board.id] = copy.deepcopy(shape)
                MainPlugin.__hover_shape[Board.id].origin_shape = shape
                MainPlugin.__hover_shape[Board.id].setColor(Qt.green)
                MainPlugin.__hover_shape[Board.id].selected = False
                return True
        MainPlugin.__hover_shape[Board.id] = None

        return False

    def checkMatch(self, mousePt, Board):
        threshold = 2.1
        allPoints = []
        # 生成所有的点列表
        for shape in MainPlugin.__shapes[Board.id]:
            allPoints += shape.getPoints()

        if MainPlugin.__state[Board.id] == MainPlugin.MOVING_SHAPE:
            allPoints.remove(MainPlugin.__changing_pt[Board.id])#在移动的时候自身 就不要匹配了 这里很耦合 之后优化的时候应该考虑解耦

        if MainPlugin.__painting_shape[Board.id]:#在把正在绘制的线的初始点给加上
            if isinstance(MainPlugin.__painting_shape[Board.id], ExLine):
                allPoints.append(MainPlugin.__painting_shape[Board.id].pt0)

        matchedX = False
        matchedY = False

        for pt in allPoints:
            if mousePt.x < pt.x+threshold and mousePt.x > pt.x-threshold:
                MainPlugin.__matched_x[Board.id] = pt.x
                matchedX = True
            if mousePt.y < pt.y + threshold and mousePt.y > pt.y - threshold:
                MainPlugin.__matched_y[Board.id] = pt.y
                matchedY = True

        if not matchedX:
            MainPlugin.__matched_x[Board.id] = None

        if not matchedY:
            MainPlugin.__matched_y[Board.id] = None

        if matchedX or matchedY:
            return True
        else:
            return False

    def getMatchedPoint(self, mousePt, Board):#其实就是综合了 hover的点 和matchedX,y 得到点
        x = mousePt.x
        y = mousePt.y
        if MainPlugin.__hover_point[Board.id]:
            x = MainPlugin.__hover_point[Board.id].x
            y = MainPlugin.__hover_point[Board.id].y
        else:
            # 没有hover到点就设置成匹配到的x,y
            if MainPlugin.__matched_y[Board.id]:
                y = MainPlugin.__matched_y[Board.id]
            if MainPlugin.__matched_x[Board.id]:
                x = MainPlugin.__matched_x[Board.id]

        return ExPoint(x,y)


    def paintEvent(self, QPaintEvent):
        Board = ExInterFace.getCurrentBoard()
        painter = QPainter(Board)
        painter.setRenderHint(QPainter.Antialiasing, True)#打开反走样
        #在坐标转换之前先绘制文字

        #坐标系转换为 x朝上和y朝右的通用数学坐标系
        painter.setWindow(0, Board.height(), Board.width(), -Board.height())
        painter.translate(MainPlugin.__origin_position[Board.id].x * MainPlugin.unit_pixel,
                          MainPlugin.__origin_position[Board.id].y * MainPlugin.unit_pixel)
        painter.scale(MainPlugin.__scale[Board.id], MainPlugin.__scale[Board.id])


        #绘制十字原点
        MainPlugin.__origin_cross.drawIt(painter, MainPlugin.__scale[Board.id])


        #绘制图形
        for shape in MainPlugin.__shapes[Board.id]:
            shape.draw(painter, MainPlugin)

        if MainPlugin.__state[Board.id] <= MainPlugin.PAINTING_CIRCLE and MainPlugin.__state[
            Board.id] >= MainPlugin.PAINTING_LINE:
            #绘制正在绘制的图形
            if MainPlugin.__painting_shape[Board.id]:
                MainPlugin.__painting_shape[Board.id].draw(painter, MainPlugin)

        if MainPlugin.__state[Board.id] == MainPlugin.PAINT_LINE:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINT_CIRCLE:
            # 在绘制圆的时候使用
            if MainPlugin.__assist_circle[Board.id]:
                MainPlugin.__assist_circle[Board.id].draw(painter, MainPlugin)
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINT_ARC:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_ARC0:
            if MainPlugin.__assist_line[Board.id]:
                MainPlugin.__assist_line[Board.id].draw(painter, MainPlugin)
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_ARC1:
            if MainPlugin.__assist_line[Board.id]:
                MainPlugin.__assist_line[Board.id].draw(painter, MainPlugin)
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_CIRCLE:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.PAINTING_LINE:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.FREE:
            pass
        elif MainPlugin.__state[Board.id] == MainPlugin.MOVING_BOARD:
            pass

        if MainPlugin.__state[Board.id] == MainPlugin.SELECT:
            if MainPlugin.__hover_shape[Board.id]:
                MainPlugin.__hover_shape[Board.id].draw(painter, MainPlugin)

        if MainPlugin.__state[Board.id]>=MainPlugin.PAINT_LINE and MainPlugin.__state[Board.id]<=MainPlugin.MOVING_SHAPE:

            # 绘制悬停对象
            if MainPlugin.__hover_point[Board.id]:
                MainPlugin.__hover_point[Board.id].draw(painter, MainPlugin)

            # 绘制 匹配到的虚线
            vLine = None
            hLine = None
            if MainPlugin.__matched_x[Board.id]:
                vLine = FreeLine(MainPlugin.__matched_x[Board.id], 0, MainPlugin.__matched_x[Board.id], Board.height())
            if MainPlugin.__matched_y[Board.id]:
                hLine = FreeLine(0, MainPlugin.__matched_y[Board.id], Board.width(), MainPlugin.__matched_y[Board.id])
            if vLine:
                vLine.draw(painter, MainPlugin)
            if hLine:
                hLine.draw(painter, MainPlugin)


    def clearCurrentVar(self):#当状态产生切换时 一些临时的变量 需要清理
        for k, v in MainPlugin.__painting_shape.items():
            MainPlugin.__painting_shape[k] = None
            MainPlugin.__hover_shape[k] = None
            MainPlugin.__hover_point[k] = None
            MainPlugin.__matched_y[k] = None
            MainPlugin.__matched_x[k] = None
            MainPlugin.__assist_circle[k] = None

    def boardInit(self, Board):#这个初始化将会延迟到 board创建的时候才会执行
        MainPlugin.__state[Board.id] = MainPlugin.FREE
        MainPlugin.__shapes[Board.id] = []
        MainPlugin.__hover_point[Board.id] = None
        MainPlugin.__hover_shape[Board.id] = None
        MainPlugin.__painting_shape[Board.id] = None
        MainPlugin.__matched_y[Board.id] = None
        MainPlugin.__matched_x[Board.id] = None
        MainPlugin.__assist_circle[Board.id] = None
        MainPlugin.__origin_position[Board.id] = ExPoint(0, 0)
        MainPlugin.__scale[Board.id] = 1
        MainPlugin.__assist_line[Board.id] = None
        MainPlugin.__changing_pt[Board.id] = None
        MainPlugin.__hand_start_pt[Board.id] = ExPoint()
        
    @pyqtSlot(int)
    def boardSwitched(self, curindex):
        Board = ExInterFace.getCurrentBoard()
        MainPlugin.__state[Board.id] = self.getCurrentSelectedState()

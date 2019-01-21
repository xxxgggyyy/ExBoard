from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import Qt
class ExShape:

    def __init__(self):
        self.color = QColor(Qt.black)#默认颜色
        self.__selected = False

    def setColor(self, color):
        self.color = color

    def draw(self, QPainter, MainPlugin):
        pass

    def getPoints(self):
        return []

    @property
    def selected(self):
        return self.__selected

    @selected.setter
    def selected(self, b):
        #在这个设置选中颜色
        self.color = QColor(Qt.green)
        self.__selected = b

    def isPointOnShape(self, pt, MainPlugin):
        pass

    def isPointNearShape(self,pt,r,MainPlugin):
        pass

    def deepCopy(self):
        return ExShape()

class ExPoint(ExShape):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.x = None
        self.y = None
        if not kwargs:
            if len(args) == 0:#无参
                return
            if len(args) == 1:#该参数为QPoint
                if isinstance(args[0], QPoint):
                    self.x = args[0].x()
                    self.y = args[0].y()
                elif isinstance(args[0], ExPoint):
                    self.x = args[0].x
                    self.y = args[0].y
                return
            if len(args)!=2:
                raise TypeError("ExPoine只需要两个参数")
            self.x = args[0]#两个参数
            self.y = args[1]
            return
        else:
            if not args:
                self.x = kwargs['x']#用x,y指定的两个参数
                self.y = kwargs['y']
                return
            else:
                raise TypeError("不能混用 指定参数的方式")

    def isPointNearShape(self,pt,r,MainPlugin):
        v = (pt.x - self.x)*(pt.x - self.x) + (pt.y - self.y)*(pt.y - self.y)
        if v <= r*r:
            return True
        else:
            return False


class ExLine(ExShape):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.pt0 = ExPoint()
        self.pt1 = ExPoint()
        if not kwargs:
            if len(args) == 0:
                return
            if len(args) == 4:#我这里没有判断参数的类型
                self.pt0.x = args[0]
                self.pt0.y = args[1]
                self.pt1.x = args[2]
                self.pt1.y = args[3]
                return
            if len(args) == 2:
                self.pt0 = args[0]
                self.pt1 = args[1]
                return
        else:
            if args:
                raise TypeError("不能混用参数")
            else:
                self.pt0 = kwargs["pt0"]
                self.pt1 = kwargs["pt1"]

    def setValue(self, *args):
        if len(args) == 2:
            self.pt0 = args[0]
            self.pt1 = args[1]
        elif len(args) == 4:
            self.pt0.x = args[0]
            self.pt0.y = args[1]
            self.pt1.x = args[2]
            self.pt1.y = args[3]
        else:
            raise TypeError("参数不正确")

    def getPoints(self):
        return [self.pt0, self.pt1]

    def setPt0(self,x,y):
        self.pt0.x = x
        self.pt0.y = y

    def setPt1(self,x,y):
        self.pt1.x = x
        self.pt1.y = y

    def draw(self, QPainter, MainPlugin):
        QPainter.save()
        #定义画笔
        pen = QPen()
        pen.setColor(self.color)
        pen.setWidth(MainPlugin.line_width)
        pen.setCapStyle(Qt.RoundCap)
        QPainter.setPen(pen)

        #绘制图形
        QPainter.drawLine(self.pt0.x*MainPlugin.unit_pixel,self.pt0.y*MainPlugin.unit_pixel,self.pt1.x*MainPlugin.unit_pixel,self.pt1.y*MainPlugin.unit_pixel)
        QPainter.restore()

    def isPointOnShape(self, pt,MainPlugin):

        #判断的阈值
        threshold = 1.5

        #计算直线的一般方程
        a = self.pt1.y - self.pt0.y
        b = self.pt0.x - self.pt1.x
        c = self.pt1.x*self.pt0.y - self.pt0.x*self.pt1.y

        result = False

        if a == 0 and b == 0:
            result = False
        elif a == 0:
            if pt.y < (-c)/b + threshold and pt.y > (-c)/b - threshold:
                result = True
            else:
                result = False
        elif b == 0:
            if pt.x < (-c)/a + threshold and pt.x  > (-c)/a  - threshold:
                result = True
            else:
                result = False
        else:
            y = ((-c) - a * pt.x) / b
            # 因为斜率不同时 其单位距离相差的值会不同 所以阈值不应该保持不变
            k = (-a)/b
            k = k if k>0 else -k#变为正值
            if k >= 1.5:#当直线变得相对垂直的时候增大阈值
                if pt.y < y + k and pt.y > y - k:
                    result = True
                else:
                    result = False
            else:
                if pt.y < y + threshold and pt.y > y - threshold:
                    result = True
                else:
                    result = False


        #上面验证了 点在直线附近 还要验证 是否在线段内
        if result:
            maxX,minX = (self.pt0.x, self.pt1.x) if self.pt0.x > self.pt1.x else (self.pt1.x, self.pt0.x)
            maxY,minY = (self.pt0.y, self.pt1.y) if self.pt0.y > self.pt1.y else (self.pt1.y, self.pt0.y)

            if a == 0:
                if pt.x <= maxX and pt.x >= minX:
                    result = True
                else:
                    result = False
            elif b == 0:
                if pt.y <= maxY and pt.y >= minY:
                    result = True
                else:
                    result = False
            else:
                if pt.x <= maxX+threshold and pt.x >= minX-threshold:
                    if pt.y <= maxY+threshold and pt.y >= minY-threshold:
                        result = True
                    else:
                        result = False
                else:
                    result = False

        return result


class ExArc(ExShape):

    def __init__(self):
        super().__init__()

class ExCircle(ExShape):

    def __init__(self):
        super().__init__()

#下面是一些 特殊图形 不是表示数据的图形 比如 坐标系的十字箭头等

class CirclePoint(ExPoint):

    HOVER = 0
    PRESSED = 1
    NONE = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.r = 2
        self.state = CirclePoint.HOVER

    def draw(self, QPainter, MainPlugin):
        QPainter.save()
        if self.state == CirclePoint.HOVER:
            self.setColor(Qt.green)
        elif self.state == CirclePoint.PRESSED:
            self.setColor(Qt.red)
        pen = QPen()
        pen.setColor(self.color)
        pen.setWidth(MainPlugin.line_width)
        QPainter.setPen(pen)
        #绘制一个圆圈
        QPainter.drawEllipse((self.x-self.r)*MainPlugin.unit_pixel, (self.y-self.r)*MainPlugin.unit_pixel, 2*self.r*MainPlugin.unit_pixel, 2*self.r*MainPlugin.unit_pixel)
        #再绘制一下中心点
        QPainter.drawPoint(self.x*MainPlugin.unit_pixel,self.y*MainPlugin.unit_pixel)

        QPainter.restore()

class FreeLine(ExLine):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.pen = QPen()
        self.pen.setColor(Qt.gray)
        self.pen.setStyle(Qt.DotLine)
        self.pen.setCapStyle(Qt.RoundCap)
        self.pen.setWidth(2)

    def setPen(self, pen):
        if pen:
            self.pen = pen

    def draw(self, QPainter, MainPlugin):
        QPainter.save()
        if self.pen:
            QPainter.setPen(self.pen)
        # 绘制图形
        QPainter.drawLine(self.pt0.x * MainPlugin.unit_pixel, self.pt0.y * MainPlugin.unit_pixel,
                              self.pt1.x * MainPlugin.unit_pixel, self.pt1.y * MainPlugin.unit_pixel)
        QPainter.restore()

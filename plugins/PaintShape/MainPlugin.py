from business import Plugin
from designs import DrawerItem, DrawerContentItem

class MainPlugin(Plugin):

    def __init__(self, name):
        super().__init__(name)
        self.__drawerItem = DrawerItem("绘图")
        self.__lineContenItem = DrawerContentItem("Line", parent=self.__drawerItem)
        self.__arcContenItem = DrawerContentItem("Arc", parent=self.__drawerItem)
        self.__circleContenItem = DrawerContentItem("Circle", parent=self.__drawerItem)
        self.__handContenItem = DrawerContentItem("Hand", parent=self.__drawerItem)
        self.__selectContenItem = DrawerContentItem("Select", parent=self.__drawerItem)

        self.__drawerItem.addContentItem(self.__lineContenItem)
        self.__drawerItem.addContentItem(self.__arcContenItem)
        self.__drawerItem.addContentItem(self.__circleContenItem)
        self.__drawerItem.addContentItem(self.__handContenItem)
        self.__drawerItem.addContentItem(self.__selectContenItem)


    def getToolItems(self):
        return [self.__drawerItem]
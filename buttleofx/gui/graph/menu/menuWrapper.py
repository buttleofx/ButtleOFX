from PySide import QtCore
from PySide.QtCore import *
from PySide.QtGui import *
# data
from buttleofx.data import ButtleDataSingleton


def createMenu(parentMenu, parentName, view):
    for pluginId in ButtleDataSingleton().get().getQObjectPluginsIdentifiersByParentPath(parentName):
        # If it is a plugin, we add it to the menu
            if ButtleDataSingleton().get().isAPlugin(pluginId[1]) == True:
                parentMenu.addAction(QAction(pluginId[0], parentMenu))
                # Else we create a new menu
            else:
                submenu = QMenu(view)
                submenu.setTitle(pluginId[0])
                parentMenu.addMenu(submenu)
                createMenu(submenu, parentName + pluginId[0] + "/", view)


class MenuWrapper(QtCore.QObject):

    # Init the MenuWrapper with the parentName of the menu
    def __init__(self, parentName, elementList, view):
        super(MenuWrapper, self).__init__(view)

        self._view = view
        self._menu = QMenu(view)
        self._menu.setTitle(parentName)

        # Create a menu based on the elementList
        if elementList != []:
            for element in elementList:
                if element != "0":
                    self._menu.addAction(QAction(element, self._menu))
                else:
                    self._menu.addSeparator()

        # Create a menu based on the parentName
        else:
            self._menu.setTitle(parentName)
            createMenu(self._menu, parentName, self._view)

    @QtCore.Slot(float, float)
    def showMenu(self, x, y):
        pos = QtCore.QPoint(x, y)
        self._menu.popup(self._view.mapToGlobal(pos))

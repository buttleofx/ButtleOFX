from PySide import QtCore
from PySide.QtCore import *
from PySide.QtGui import *


class MenuWrapper(QtCore.QObject):

    # Init the MenuWrapper with the parentName of the menu
    def __init__(self, parentName, elementList, view):
        super(MenuWrapper, self).__init__(view)

        self._view = view
        self._menu = QMenu()
        self._menu.setTitle(parentName)

        for element in elementList:
            if element != "0":
                self._menu.addAction(QAction(element, self._menu))
            else:
                self._menu.addSeparator()

    @QtCore.Slot(float, float)
    def showMenu(self, x, y):
        pos = QtCore.QPoint(x, y)
        self._menu.popup(self._view.mapToGlobal(pos))

    # @QtCore.Slot()
    # def hideMenu(self):
        # print "hide"
        # self._menu.setVisible(False)

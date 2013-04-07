from PySide import QtCore
from PySide.QtCore import *
from PySide.QtGui import *
# data
from buttleofx.data import ButtleDataSingleton


class MenuWrapper(QtCore.QObject):

    # Init the MenuWrapper with the parentName of the menu
    def __init__(self, parentName, elementList, view):
        super(MenuWrapper, self).__init__(view)

        self._view = view
        self._menu = QMenu()
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
            # We get the list of the plugins for whose parent is parenName
            for pluginId in ButtleDataSingleton().get().getQObjectPluginsIdentifiersByParentPath(parentName):
                # If it is a plugin, we add it to the menu
                if ButtleDataSingleton().get().isAPlugin(pluginId[1]) == True:
                    self._menu.addAction(QAction(truc[0], self._menu))
                # Else we create a new menu
                else:
                    submenu = QMenu()
                    submenu.setTitle(pluginId[0])
                    self._menu.addMenu(submenu)
                    # And we iterate
                    for element in ButtleDataSingleton().get().getQObjectPluginsIdentifiersByParentPath(parentName + pluginId[0] + "/"):
                        if ButtleDataSingleton().get().isAPlugin(element[1]) == True:
                            self.submenu.addAction(QAction(truc[0], submenu))
                        else:
                            submenu2 = QMenu()
                            submenu2.setTitle(element[0])
                            submenu.addMenu(submenu2)

                            for truc in ButtleDataSingleton().get().getQObjectPluginsIdentifiersByParentPath(parentName + pluginId[0] + "/" + element[0] + "/"):
                                if ButtleDataSingleton().get().isAPlugin(truc[1]) == True:
                                    submenu2.addAction(QAction(truc[0], submenu2))
                                else:
                                    submenu3 = QMenu()
                                    submenu3.setTitle(truc[0])
                                    submenu2.addMenu(submenu3)

                                    for toto in ButtleDataSingleton().get().getQObjectPluginsIdentifiersByParentPath(parentName + pluginId[0] + "/" + element[0] + "/" + truc[0] + "/"):
                                        if ButtleDataSingleton().get().isAPlugin(toto[1]) == True:
                                            submenu3.addAction(QAction(toto[0], submenu3))
                                        else:
                                            submenu4 = QMenu()
                                            submenu4.setTitle(toto[0])
                                            submenu3.addMenu(submenu4)

    @QtCore.Slot(float, float)
    def showMenu(self, x, y):
        pos = QtCore.QPoint(x, y)
        self._menu.popup(self._view.mapToGlobal(pos))

    # @QtCore.Slot()
    # def hideMenu(self):
        # print "hide"
        # self._menu.setVisible(False)

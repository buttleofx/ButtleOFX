from PySide import QtCore
from PySide.QtCore import *
from PySide.QtGui import *
# data
from buttleofx.data import ButtleDataSingleton
# manager
from buttleofx.manager import ButtleManagerSingleton


def createMenu(parentMenu, parentName, view):
    for pluginId in ButtleDataSingleton().get().getQObjectPluginsIdentifiersByParentPath(parentName):
        # If it is a plugin, we add it to the menu
            if ButtleDataSingleton().get().isAPlugin(pluginId[1]) == True:
                parentMenu.addAction(QAction(pluginId[0], parentMenu, triggered=ButtleManagerSingleton().get().nodeManager.creationNodeImage))

            # Else we create a new menu
            else:
                submenu = QMenu(view)
                submenu.setTitle(pluginId[0])
                parentMenu.addMenu(submenu)
                createMenu(submenu, parentName + pluginId[0] + "/", view)


class MenuWrapper(QtCore.QObject):

    # Init the MenuWrapper with the parentName of the menu
    def __init__(self, parentName, elementList, view, app):
        super(MenuWrapper, self).__init__(view)

        self._view = view
        # self._parentName = parentName
        # self._elementList = elementList
        self._menu = QMenu(view)
        self._menu.setTitle(parentName)

        # Create a menu based on the elementList
        if elementList != []:
            for element in elementList:
                print element
                if element != "0":
                    # action = QAction(self._menu)
                    # action = self._menu.addAction(QAction(element[0], self._menu))
                    # FileMenu
                    if(element[0] == "Open"):
                        self._menu.addAction(QAction(element[0], self._menu, shortcut=element[1], statusTip='Open ', triggered=app.quit))

                    # elif(element[0] == "Save as"):
                    #     self._menu.addAction(QAction(element[0], self._menu, shortcut=element[1], statusTip='Exit the application', triggered=app.quit))

                    # elif(element[0] == "Save"):
                    #     self._menu.addAction(QAction(element[0], self._menu, shortcut=element[1], statusTip='Exit the application', triggered=app.quit))

                    # elif(element[0] == "Import"):
                    #     self._menu.addAction(QAction(element[0], self._menu, shortcut=element[1], statusTip='Load a graph', triggered=ButtleDataSingleton().get().loadData(finderLoadGraph.propFile)))

                    # elif(element[0] == "Export"):
                    #     self._menu.addAction(QAction(element[0], self._menu, shortcut=element[1], statusTip='Save graph', triggered=ButtleDataSingleton().get().saveData(finderSaveGraph.propFile)))

                    elif(element[0] == "Exit"):
                        self._menu.addAction(QAction(element[0], self._menu, shortcut=element[1], statusTip='Exit the application', triggered=app.quit))

                    # EditMenu
                    elif(element[0] == "Undo"):
                        self._menu.addAction(QAction(element[0], self._menu, shortcut=element[1], statusTip='Undo the last action', triggered=ButtleManagerSingleton().get().undo))
                    elif(element[0] == "Redo"):
                        self._menu.addAction(QAction(element[0], self._menu, shortcut=element[1], statusTip='Redo the last action', triggered=ButtleManagerSingleton().get().redo))
                    elif(element[0] == "Copy"):
                        self._menu.addAction(QAction(element[0], self._menu, shortcut=element[1], statusTip='Undo the last action', triggered=ButtleManagerSingleton().get().nodeManager.copyNode))
                    elif(element[0] == "Paste"):
                        self._menu.addAction(QAction(element[0], self._menu, shortcut=element[1], statusTip='Undo the last action', triggered=ButtleManagerSingleton().get().nodeManager.pasteNode))
                    elif(element[0] == "Cut"):
                        self._menu.addAction(QAction(element[0], self._menu, shortcut=element[1], statusTip='Undo the last action', triggered=ButtleManagerSingleton().get().nodeManager.cutNode))
                    elif(element[0] == "Duplicate"):
                        self._menu.addAction(QAction(element[0], self._menu, shortcut=element[1], statusTip='Undo the last action', triggered=ButtleManagerSingleton().get().nodeManager.duplicationNode))

                    else:
                        self._menu.addAction(QAction(element[0], self._menu, shortcut=element[1]))

                else:
                    self._menu.addSeparator()

        # Create a menu based on the parentName
        else:
            self._menu.setTitle(parentName)
            createMenu(self._menu, parentName, self._view)

             # AddMenu
            print self._menu.title()
            #self._menu.addAction(QAction(element[0], self._menu, shortcut=element[1], statusTip='Undo the last action', triggered=ButtleManagerSingleton().get().nodeManager.creationNode(nodeType, -graph.originX + 20, -graph.originY + 20)))
        

    @QtCore.Slot(float, float)
    def showMenu(self, x, y):
        # # Create a menu based on the elementList
        # if self._elementList != []:
        #     for element in self._elementList:
        #         if element != "0":
        #             self._menu.addAction(QAction(element, self._menu))
        #         else:
        #             self._menu.addSeparator()

        # # Create a menu based on the parentName
        # else:
        #     self._menu.setTitle(self._parentName)
        #     createMenu(self._menu, self._parentName, self._view)

        pos = QtCore.QPoint(x, y)
        self._menu.exec_(self._view.mapToGlobal(pos))

    def signalAction(self):
        print 'Signal Action'

    @QtCore.Slot()
    def hideMenu(self):
        self._menu.clear()

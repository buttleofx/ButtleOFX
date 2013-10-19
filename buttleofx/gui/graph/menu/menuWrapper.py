from PyQt5 import QtCore
from PyQt5 import QtGui

# TODO: no * in imports
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# data
from buttleofx.data import ButtleDataSingleton
# manager
from buttleofx.manager import ButtleManagerSingleton


def createMenu(parentMenu, parentName, view):
    for menuItem in ButtleDataSingleton().get().getQObjectPluginsIdentifiersByParentPath(parentName):
        """
            TODO : Need to be documented.
        """
        # menuItem is a tuple : see getPluginsIdentifiersAsDictionary() is data/tuttleTools.py        
        pluginParent, pluginId = menuItem  # if the item is not a plugin, pluginId = ""

        isAPlugin = ButtleDataSingleton().get().isAPlugin(pluginId) is True
        noPluginFound = pluginId is False

        if noPluginFound:
            action = QAction(pluginParent, parentMenu)
            action.setData(None)
            parentMenu.addAction(action)
        # If it is a plugin, we add it to the menu
        elif isAPlugin:
            action = QAction(pluginParent, parentMenu)
            action.setData(pluginId)
            parentMenu.addAction(action)
        # Else we create a new menu
        else:
            submenu = QMenu()  #QMenu(view)
            submenu.setTitle(pluginParent)
            parentMenu.addMenu(submenu)
            createMenu(submenu, parentName + pluginParent + "/", view)


class MenuWrapper(QtCore.QObject):
    """
             TODO : Need to be documented.
    """
    # Init the MenuWrapper with the parentName of the menu
    def __init__(self, parentName, check, view, app):
        super(MenuWrapper, self).__init__(view)
        self._view = view
        self._menu = QMenu()  #QMenu(view)
        self._menu.setTitle(parentName)

        if(check == 0):
            # File Menu
            if(parentName == 'file'):
                action = QAction("Open", self._menu,  statusTip='Open a graph')
                action.setData(0)
                self._menu.addAction(action)
                action = QAction("Save", self._menu, shortcut='Ctrl+S', statusTip='Save the graph')
                action.setData(0)
                self._menu.addAction(action)
                self._menu.addSeparator()

                action = QAction("Exit", self._menu, statusTip='Exit the application', triggered=app.quit)
                action.setData(0)
                self._menu.addAction(action)

            # EditMenu
            elif(parentName == 'edit'):
                action = QAction("Undo", self._menu, shortcut='Ctrl+Z', statusTip='Undo the last action', triggered=ButtleManagerSingleton().get().undo)
                action.setData(0)
                self._menu.addAction(action)
                action = QAction("Redo", self._menu, shortcut='Ctrl+Y', statusTip='Redo the last action', triggered=ButtleManagerSingleton().get().redo)
                action.setData(0)
                self._menu.addAction(action)
                self._menu.addSeparator()

                action = QAction("Copy", self._menu, shortcut='Ctrl+C', statusTip='Copy the selected node', triggered=ButtleManagerSingleton().get().nodeManager.copyNode)
                action.setData(0)
                self._menu.addAction(action)
                action = QAction("Paste", self._menu, shortcut='Ctrl+V', statusTip='Paste the selected node', triggered=ButtleManagerSingleton().get().nodeManager.pasteNode)
                action.setData(0)
                self._menu.addAction(action)
                action = QAction("Cut", self._menu, shortcut='Ctrl+X', statusTip='Cut the selected node', triggered=ButtleManagerSingleton().get().nodeManager.cutNode)
                action.setData(0)
                self._menu.addAction(action)
                action = QAction("Duplicate", self._menu, shortcut='Ctrl+D', statusTip='Duplicate the selected node', triggered=ButtleManagerSingleton().get().nodeManager.duplicationNode)
                action.setData(0)
                self._menu.addAction(action)
                action = QAction("Delete", self._menu, statusTip='Delete the selected node', triggered=ButtleManagerSingleton().get().deleteSelection)
                action.setData(0)
                self._menu.addAction(action)

        #Create a menu based on the parentName
        else:
            self._menu.setTitle(parentName)
            createMenu(self._menu, parentName, self._view)

        self._menu.triggered.connect(self.menuSelection)

    @QtCore.pyqtSlot(QAction)
    def menuSelection(self, action):
        """
             TODO : Need to be documented.
        """
        if action.data() is not None:
            # If it cames from the other menus
            if action.data() == 0:
                if(action.triggered is not None):
                    action.triggered.emit()
                # elif(action.text() == "Delete"):
                #     if(ButtleDataSingleton().get().currentConnectionWrapper):
                #         ButtleManagerSingleton().get().connectionManager.disconnect(ButtleDataSingleton().get().currentConnectionWrapper)
                #     else:
                #         ButtleManagerSingleton().get().nodeManager.destructionNodes()

            # If it cames from the NodeMenu
            else:
                ButtleManagerSingleton().get().nodeManager.creationNode(action.data())

    @QtCore.pyqtSlot(float, float)
    def showMenu(self, x, y):
        """
             TODO : Need to be documented.
        """
        pos = QtCore.QPoint(x, y)
        self._menu.exec_(self._view.mapToGlobal(pos))

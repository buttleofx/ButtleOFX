from PyQt5 import QtGui
from PyQt5 import QtCore

from buttleofx.data import globalButtleData
from buttleofx.manager import globalButtleManager


def createMenu(parentMenu, parentName, view):
    for menuItem in globalButtleData.getQObjectPluginsIdentifiersByParentPath(parentName):
        """
            TODO : Need to be documented.
        """
        # menuItem is a tuple : see getPluginsIdentifiersAsDictionary() is data/tuttleTools.py
        pluginParent, pluginId = menuItem  # If the item is not a plugin, pluginId = ""

        isAPlugin = globalButtleData.isAPlugin(pluginId) is True
        noPluginFound = pluginId is False

        if noPluginFound:
            action = QtCore.QAction(pluginParent, parentMenu)
            action.setData(None)
            parentMenu.addAction(action)
        # If it is a plugin, we add it to the menu
        elif isAPlugin:
            action = QtCore.QAction(pluginParent, parentMenu)
            action.setData(pluginId)
            parentMenu.addAction(action)
        # Else we create a new menu
        else:
            submenu = QtGui.QMenu()  # QtGui.QMenu(view)
            submenu.setTitle(pluginParent)
            parentMenu.addMenu(submenu)
            createMenu(submenu, parentName + pluginParent + "/", view)


class MenuWrapper(QtCore.QObject):
    """
             TODO : Need to be documented.
    """
    # Initialize the MenuWrapper with the parentName of the menu
    def __init__(self, parentName, check, view, app):
        super(MenuWrapper, self).__init__(view)
        self._view = view
        self._menu = QtGui.QMenu()  # QtGui.QMenu(view)
        self._menu.setTitle(parentName)

        if check == 0:
            # File Menu
            if parentName == 'file':
                action = QtCore.QAction(
                    "Open", self._menu,
                    statusTip='Open a graph')
                action.setData(0)
                self._menu.addAction(action)

                action = QtCore.QAction(
                    "Save", self._menu, shortcut='Ctrl+S',
                    statusTip='Save the graph')
                action.setData(0)
                self._menu.addAction(action)
                self._menu.addSeparator()

                action = QtCore.QAction(
                    "Exit", self._menu,
                    statusTip='Exit the application',
                    triggered=app.quit)
                action.setData(0)
                self._menu.addAction(action)

            # EditMenu
            elif parentName == 'edit':
                action = QtCore.QAction(
                    "Undo", self._menu, shortcut='Ctrl+Z',
                    statusTip='Undo the last action',
                    triggered=globalButtleManager.undo)
                action.setData(0)
                self._menu.addAction(action)
                action = QtCore.QAction(
                    "Redo", self._menu, shortcut='Ctrl+Y',
                    statusTip='Redo the last action',
                    triggered=globalButtleManager.redo)
                action.setData(0)
                self._menu.addAction(action)
                self._menu.addSeparator()

                action = QtCore.QAction(
                    "Copy", self._menu, shortcut='Ctrl+C',
                    statusTip='Copy the selected node',
                    triggered=globalButtleManager.nodeManager.copyNode)
                action.setData(0)
                self._menu.addAction(action)

                action = QtCore.QAction(
                    "Paste", self._menu, shortcut='Ctrl+V',
                    statusTip='Paste the selected node',
                    triggered=globalButtleManager.nodeManager.pasteNode)
                action.setData(0)
                self._menu.addAction(action)

                action = QtCore.QAction(
                    "Cut", self._menu, shortcut='Ctrl+X',
                    statusTip='Cut the selected node',
                    triggered=globalButtleManager.nodeManager.cutNode)
                action.setData(0)
                self._menu.addAction(action)

                action = QtCore.QAction(
                    "Duplicate", self._menu, shortcut='Ctrl+D',
                    statusTip='Duplicate the selected node',
                    triggered=globalButtleManager.nodeManager.duplicationNode)
                action.setData(0)
                self._menu.addAction(action)

                action = QtCore.QAction(
                    "Delete", self._menu,
                    statusTip='Delete the selected node',
                    triggered=globalButtleManager.deleteSelection)
                action.setData(0)
                self._menu.addAction(action)

        # Create a menu based on the parentName
        else:
            self._menu.setTitle(parentName)
            createMenu(self._menu, parentName, self._view)

        self._menu.triggered.connect(self.menuSelection)

    @QtCore.pyqtSlot(QtCore.QAction)
    def menuSelection(self, action):
        """
             TODO : Need to be documented.
        """
        if action.data() is not None:
            # If it comes from the other menus
            if action.data() == 0:
                # if action.triggered is not None:
                    action.trigger.connect()
                    action.triggered.emit()
                    # self.connect(action, SIGNAL(triggered(bool)), this, SLOT(app.quit))
                # elif action.text() == "Delete":
                #     if globalButtleData.currentConnectionWrapper:
                #         globalButtleManager.connectionManager.disconnect(
                #             globalButtleData.currentConnectionWrapper)
                #     else:
                #         globalButtleManager.nodeManager.destructionNodes()

            # If it cames from the NodeMenu
            # else:
                # globalButtleManager.nodeManager.creationNode(action.data())

    @QtCore.pyqtSlot(float, float)
    def showMenu(self, x, y):
        """
             TODO : Need to be documented.
        """
        pos = QtCore.QPoint(x, y)
        self._menu.exec_(self._view.mapToGlobal(pos))

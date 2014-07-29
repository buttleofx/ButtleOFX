from PyQt5 import QtCore, QtGui
from quickmamba.models import QObjectListModel


class Shortcut(QtCore.QObject):
    """
        Class Shortcuts
        _shortcutKeys: keys to press
        _shortcutName: name of the shortcutKeys
        _shortcutDoc: explanation of the shortcutKeys
        _shortcutContent: in which case this shortcut can be used
    """

    def __init__(self, shortcutKey1, shortcutKey2, shortcutName, shortcutDoc, shortcutContext):
        QtCore.QObject.__init__(self)

        self._shortcutKey1 = shortcutKey1
        self._shortcutKey2 = shortcutKey2
        self._shortcutName = shortcutName
        self._shortcutDoc = shortcutDoc
        self._shortcutContext = shortcutContext

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getShortcutContext(self):
        return self._shortcutContext

    def getShortcutDoc(self):
        return self._shortcutDoc

    def getShortcutKey1(self):
        return self._shortcutKey1

    def getShortcutKey2(self):
        return self._shortcutKey2

    def getShortcutName(self):
        return self._shortcutName

    # ## Setters ## #

    def setShortcutContext(self, context):
        self._shortcutContext = context

    def setShortcutDoc(self, doc):
        self._shortcutDoc = doc

    def setShortcutKey1(self, key):
        self._shortcutKeys = key

    def setShortcutKey2(self, key):
        self._shortcutKeys = key

    def setShortcutName(self, name):
        self._shortcutName = name

    # ############################################# Data exposed to QML ############################################## #

    changed = QtCore.pyqtSignal()
    shortcutKey1 = QtCore.pyqtProperty(str, getShortcutKey1, setShortcutKey1, constant=True)
    shortcutKey2 = QtCore.pyqtProperty(str, getShortcutKey2, setShortcutKey2, constant=True)
    shortcutName = QtCore.pyqtProperty(str, getShortcutName, setShortcutName, constant=True)
    shortcutDoc = QtCore.pyqtProperty(str, getShortcutDoc, setShortcutDoc, constant=True)
    shortcutContext = QtCore.pyqtProperty(str, getShortcutContext, setShortcutContext, constant=True)

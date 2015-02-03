from PyQt5 import QtCore
from buttleofx.gui.browser_v2.browserModel import BrowserModel


class BrowserTree(QtCore.QObject):
    def __init__(self):
        self._model = BrowserModel()
        self._subModel = None
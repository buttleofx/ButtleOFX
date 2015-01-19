import os
from enum import Enum
from PyQt5 import QtCore


class BrowserItem(QtCore.QObject):
    class ItemType(Enum):
        file = 1
        folder = 2
        sequence = 3

    # class Status(Enum):
    #    pass

    _isSelected = False
    _sequence = None
    _weight = 0.0
    _fileExtension = ""

    # gui operations, int for the moment
    _actionStatus = 0

    statusChanged = QtCore.pyqtSignal()
    selectedChanged = QtCore.pyqtSignal()

    def __init__(self, dirAbsolutePath, nameItem, typeItem, supported):
        super(BrowserItem, self).__init__()

        self._path = os.path.join(dirAbsolutePath, nameItem)
        self._typeItem = typeItem
        self._supported = supported

        if typeItem == BrowserItem.ItemType.folder:
            # script from qml path: 1 level higher
            self._pathImg = "../../img/buttons/browser/folder-icon.png"

        elif typeItem == BrowserItem.ItemType.file:
            self._fileExtension = os.path.splitext(nameItem)[1]
            if supported:
                self._fileImg = 'image://buttleofx/' + self._filepath
            else:
                self._fileImg = "../../img/buttons/browser/file-icon.png"

            # May throw exception on bad symlink
            try:
                self._weight = os.stat(self._path).st_size
            except FileNotFoundError:
                pass

        elif typeItem == BrowserItem.ItemType.sequence:
            # waiting sequenceParser
            pass

    def notifyAddAction(self):
        self._actionStatus += 1
        self.statusChanged.emit()

    def notifyRemoveAction(self):
        self._actionStatus -= 1
        self.statusChanged.emit()

    def getSelected(self):
        return self._isSelected

    def setSelected(self, selected):
        self._isSelected = selected
        self.selectedChanged.emit()

    def getWeight(self):
        return self._weight

    def getFileExtension(self):
        return self._fileExtension

    def getPathImg(self):
        return self._pathImg

    def getSequence(self):
        return self._sequence

    def getName(self):
        return os.path.dirname(self._path)

    def isRemoved(self):
        return os.path.exists(self._path)

    # ############################################ Methods exposed to QML ############################################ #

    @QtCore.pyqtSlot(result=list)
    def getActionStatus(self):
        return self._actionStatus

    @QtCore.pyqtSlot(result=str)
    def getPath(self):
        return self._path

    @QtCore.pyqtSlot(result=int)
    def getType(self):
        return self._typeItem

    # ################################### Data exposed to QML #################################### #

    isSelected = QtCore.pyqtProperty(bool, getSelected, setSelected, notify=selectedChanged)
    actionStatus = QtCore.pyqtProperty(list, getActionStatus, notify=statusChanged)

    path = QtCore.pyqtProperty(str, getPath, constant=True)
    type = QtCore.pyqtProperty(int, getType, constant=True)
    weight = QtCore.pyqtProperty(float, getWeight, constant=True)
    pathImg = QtCore.pyqtProperty(str, getPathImg, constant=True)
    name = QtCore.pyqtProperty(str, getName, constant=True)

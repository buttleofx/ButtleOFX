import os
from PyQt5 import QtCore
from datetime import datetime
from pwd import getpwuid
from stat import filemode

class BrowserItem(QtCore.QObject):
    class ItemType:
        file = 1
        folder = 2
        sequence = 3

    # class Status:
    #    pass

    _isSelected = False
    _sequence = None
    _weight = 0.0
    _fileExtension = ""
    _owner = ""
    _lastModification = ""
    _permissions = ""

    # gui operations, int for the moment
    _actionStatus = 0

    statusChanged = QtCore.pyqtSignal()
    selectedChanged = QtCore.pyqtSignal()
    fileChanged = QtCore.pyqtSignal()

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
                self._fileImg = 'image://buttleofx/' + self._path
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

        if not typeItem == BrowserItem.ItemType.sequence:
            try:
                self._lastModification = datetime.fromtimestamp(os.stat(self._path).st_mtime).strftime("%c")
                self._permissions = self.getPermissionsOnFileSystem()
                self._owner = self.getOwnerOnFileSystem()
            except:
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

    def getParentPath(self):
        return os.path.dirname(self._path)

    def getName(self):
        return os.path.basename(self._path)

    def isRemoved(self):
        return os.path.exists(self._path)

    def getLastModification(self):
        return self._lastModification

    def updatePath(self, newPath):
        self._path = newPath
        self.fileChanged.emit()

    def updatePermissions(self):
        try:
            self._permissions = self.getPermissionsOnFileSystem()
            self.fileChanged.emit()
        except:
            pass

    def updateOwner(self):
        self._owner = self.getOwnerOnFileSystem()
        self.fileChanged.emit()

    def getOwnerOnFileSystem(self):
        return getpwuid(os.stat(self._path).st_uid).pw_name

    def getPermissionsOnFileSystem(self):
        return filemode(os.stat(self._path).st_mode)

    def isFile(self):
        return self._typeItem == BrowserItem.ItemType.file

    def isFolder(self):
        return self._typeItem == BrowserItem.ItemType.folder

    def isSequence(self):
        return self._typeItem == BrowserItem.ItemType.sequence

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

    @QtCore.pyqtSlot(result=str)
    def getPermissions(self):
        return self._permissions

    @QtCore.pyqtSlot(result=str)
    def getOwner(self):
        return self._owner

    # ################################### Data exposed to QML #################################### #

    isSelected = QtCore.pyqtProperty(bool, getSelected, setSelected, notify=selectedChanged)
    actionStatus = QtCore.pyqtProperty(list, getActionStatus, notify=statusChanged)

    path = QtCore.pyqtProperty(str, getPath, updatePath, notify=fileChanged)
    type = QtCore.pyqtProperty(int, getType, constant=True)
    weight = QtCore.pyqtProperty(float, getWeight, constant=True)
    pathImg = QtCore.pyqtProperty(str, getPathImg, constant=True)
    name = QtCore.pyqtProperty(str, getName, constant=True, notify=fileChanged)
    permissions = QtCore.pyqtProperty(str, getPermissions, constant=True, notify=fileChanged)
    owner = QtCore.pyqtProperty(str, getOwner, constant=True, notify=fileChanged)

from PyQt5 import QtCore


class SortOn(QtCore.QObject):
        # enum contains string for easy use from qml
        onName = "onName"
        onSize = "onSize"

        def __init__(self):
            super(SortOn, self).__init__()
            self._fieldToSort = self.onName
            self._reverse = 0

        @QtCore.pyqtSlot(result=str)
        def getFieldToSort(self):
            return self._fieldToSort

        @QtCore.pyqtSlot(result=bool)
        def isReversed(self):
            return self._reverse

        @QtCore.pyqtSlot(str, int)
        def setFieldToSort(self, newField, reverse=0):
            if newField != self.onName and newField != self.onSize:
                raise Exception("Sort on: bad field")

            self._fieldToSort = newField
            self._reverse = reverse
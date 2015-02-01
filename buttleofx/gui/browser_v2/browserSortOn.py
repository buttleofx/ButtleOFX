from PyQt5 import QtCore


class SortOn(QtCore.QObject):
        # enum contains string for easy use from qml
        onName = "onName"
        onSize = "onSize"
        onType = "onType"

        # list for easy check while setting field sort
        masks = [onName, onSize, onType]

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
            fieldFound = False
            for field in self.masks:
                if newField == field:
                    fieldFound =True
                    break

            if not fieldFound:
                raise Exception("Sort on: bad field")

            self._fieldToSort = newField
            self._reverse = reverse
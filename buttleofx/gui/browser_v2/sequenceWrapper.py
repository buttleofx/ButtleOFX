import os
from PyQt5 import QtCore
from pySequenceParser import sequenceParser


class SequenceWrapper(QtCore.QObject):

    def __init__(self, sequenceParserItem, absPath, parent=None):
        super(SequenceWrapper, self).__init__(parent)
        self._sequence = sequenceParserItem.getSequence().clone()  # copy object
        self._firstFilePath = os.path.join(os.path.dirname(absPath), self._sequence.getFirstFilename())
        self._weight = sequenceParser.ItemStat(sequenceParserItem).sizeOnDisk

    def getNbFiles(self):
        return self._sequence.getNbFiles()

    def getFirstFilePath(self):
        return self._firstFilePath

    def getSequenceParsed(self):
        return self._sequence

    def getWeight(self):
        return self._weight

    # ################################### Data exposed to QML #################################### #
    weight = QtCore.pyqtProperty(int, getWeight)
    firstFilePath = QtCore.pyqtProperty(str, getFirstFilePath)
    nbFiles = QtCore.pyqtProperty(int, getNbFiles)
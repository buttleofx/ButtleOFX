import os
from PyQt5 import QtCore
from pySequenceParser import sequenceParser


class SequenceWrapper(QtCore.QObject):

    def __init__(self, sequence, absPath, parent=None):
        super(SequenceWrapper, self).__init__(parent)
        self._sequence = sequence.clone()  # copy object
        self._firstFilePath = os.path.join(os.path.dirname(absPath), sequence.getFirstFilename())

    def getNbFiles(self):
        return self._sequence.getNbFile()

    def getFirstFilePath(self):
        return self._firstFilePath

    def getSequenceParsed(self):
        return self._sequence

import os
from PyQt5 import QtCore


class SequenceWrapper(QtCore.QObject):

    def __init__(self, sequence, absPath):
        super(SequenceWrapper, self).__init()
        self._sequence = sequence
        self._firstFilePath = os.path.join(os.dirname(absPath), sequence.getFirstFilename())

    def getNbFiles(self):
        return self._sequence.getNbFile()

    def getFirstFilePath(self):
        return self._firstFilePath


from PyQt5 import QtCore
import logging
import os
# quickmamba
from quickmamba.models import QObjectListModel


class SequenceWrapper(QtCore.QObject):
    """
        Class SequenceWrapper defined by :
            - _sequence : a sequence of images
    """
    
    def __init__(self, sequence):
        super(SequenceWrapper, self).__init__()
        
        self._sequence = sequence
        
    def __str__(self):
        return 'Test'
    
    ########################################## Getters ##########################################
    def getFirstFilePath(self):
        return self._sequence.getAbsoluteFirstFilename()
    
    def getFirstFileName(self):
        return self._sequence.getFirstFilename()
    
    @QtCore.pyqtSlot(result=int)
    def getNbFiles(self):
        return self._sequence.getNbFiles()
        
    def getWeight(self):
        res = 0
        for i in range(self._sequence.getFirstTime(), self._sequence.getLastTime() + self._sequence.getStep(), self._sequence.getStep()):
            fullpath = self._sequence.getAbsoluteFilenameAt(i)
            if os.path.exists(fullpath):
                res = res + os.stat(fullpath).st_size
        return (res) / self._sequence.getNbFiles()
        
    def getTime(self):
        return self._sequence.getDuration()
        
    ##################################### DATA EXPOSED TO QML ######################################
    firstFilePath = QtCore.pyqtProperty(str, getFirstFilePath, constant=True)
    firstFileName = QtCore.pyqtProperty(str, getFirstFileName, constant=True)
    nbFiles = QtCore.pyqtProperty(int, getNbFiles, constant=True)
    weight = QtCore.pyqtProperty(float, getWeight, constant=True)
    time = QtCore.pyqtProperty(float, getTime, constant=True)
    
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

class ScreenPicker(QtCore.QObject):
    """
        Define the common methods and fields for paramWrappers.
    """

    def __init__(self, parent = None):
        QtCore.QObject.__init__(self, parent)
        self._testColor = "#AFE121"


    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getTestColor(self):
        return self._testColor

    def setTestColor(self, testColor):
        print ("python test "+testColor)
        self._testColor = testColor
        self.testColorChange.emit()

    # ## Others ## #
    @QtCore.pyqtSlot(result=QtGui.QColor)
    def startGrabColor(self):
        print("start grab color")
        desktop = QtWidgets.QDesktopWidget()
        cursor = QtGui.QCursor()
        pixmap = QtGui.QGuiApplication.screens()[desktop.screenNumber()].grabWindow(desktop.winId(), cursor.pos().x(), cursor.pos().y(), 1, 1)
        qImage = pixmap.toImage()
        qColor = QtGui.QColor(qImage.pixel(0, 0))
        return qColor




    # ############################################# Data exposed to QML ############################################## #

    testColorChange = QtCore.pyqtSignal()
    testColor = QtCore.pyqtProperty(str, getTestColor, setTestColor, notify=testColorChange)

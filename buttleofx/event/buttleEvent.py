from PyQt5 import QtCore
from quickmamba.patterns import Signal


class ButtleEvent(QtCore.QObject):
    """
        Class ButtleEvent defined by:
            - paramChangedSignal : signal emited when a param value changed
            - viewerChangedSignal : signal emited when the current view of the viewer changes

        This class contains all data we need to manage the application.
    """

    # Signals
    oneParamChangedSignal = Signal()
    viewerChangedSignal = Signal()

    # ############################################ Methods exposed to QML ############################################ #

    @QtCore.pyqtSlot()
    def emitViewerChangedSignal(self):
        """
            Emits the signal viewerChangedSignal.
        """
        self.viewerChangedSignal()

    # ######################################## Methods private to this class ####################################### #

    def emitOneParamChangedSignal(self):
        """
            Emits the signal paramChangedSignal.
        """
        self.oneParamChangedSignal()


globalButtleEvent = ButtleEvent()


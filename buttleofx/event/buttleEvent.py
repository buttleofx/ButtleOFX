from PySide import QtCore, QtGui
# quickmamba
from quickmamba.patterns import Singleton, Signal
# tools
from buttleofx.data import tuttleTools


class ButtleEvent(QtCore.QObject):
    """
        Class ButtleEvent defined by:
            - paramChangedSignal : signal emited when a param value changed
            - viewerChangedSignal : signal emited when the current view of the viewer changes

        This class contains all data we need to manage the application.
    """

    # signals
    oneParamChangedSignal = Signal()
    viewerChangedSignal = Signal()

    ### emit signals ###

    def emitOneParamChangedSignal(self):
        """
            Emits the signal paramChangedSignal.
        """
        self.oneParamChangedSignal()

    @QtCore.Slot()
    def emitViewerChangedSignal(self):
        """
            Emits the signal viewerChangedSignal.
        """
        self.viewerChangedSignal()


# This class exists just because thre are problems when a class extends 2 other class (Singleton and QObject)
class ButtleEventSingleton(Singleton):

    _buttleEvent = ButtleEvent()

    def get(self):
        return self._buttleEvent

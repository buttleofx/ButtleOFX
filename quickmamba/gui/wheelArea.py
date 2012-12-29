from PySide import QtCore
from PySide import QtDeclarative

class WheelArea(QtDeclarative.QDeclarativeItem):
    #QPointF pos, int delta, Qt::MouseButtons buttons, Qt::KeyboardModifiers modifiers
    internVerticalWheel = QtCore.Signal(QtCore.QPointF, int, QtCore.Qt.MouseButtons, QtCore.Qt.KeyboardModifiers)
    internHorizontalWheel = QtCore.Signal(QtCore.QPointF, int, QtCore.Qt.MouseButtons, QtCore.Qt.KeyboardModifiers)
  
    def __init__(self, parent = None):
        QtDeclarative.QDeclarativeItem.__init__(self, parent)

    def wheelEvent(self, event):
        if event.orientation() == QtCore.Qt.Horizontal:
            self.internHorizontalWheel.emit(event.pos(), event.delta(), event.buttons(), event.modifiers())
        elif event.orientation() == QtCore.Qt.Vertical:
            self.internVerticalWheel.emit(event.pos(), event.delta(), event.buttons(), event.modifiers())
        else:
            event.ignore()


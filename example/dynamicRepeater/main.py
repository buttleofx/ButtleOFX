import sys
sys.path.append("../..")

from PySide import QtCore, QtGui, QtDeclarative
from quickmamba.models import QObjectListModel


class ClipWrapper(QtCore.QObject):
    def __init__(self, name, duration):
        super(ClipWrapper, self).__init__()
        self._name = name
        self._duration = duration

    def getName(self):
        return self._name

    def getDuration(self):
        return self._duration

    nameChanged = QtCore.Signal()
    durationChanged = QtCore.Signal()
    name = QtCore.Property(str, getName, notify=nameChanged)
    duration = QtCore.Property(int, getDuration, notify=durationChanged)


class MainWrapper(QtCore.QObject):
    def __init__(self, parent):
        super(MainWrapper, self).__init__(parent)
        self._clips = QObjectListModel(self)
        self._clips.setObjectList([ClipWrapper("Clip0", 2.2), ClipWrapper("Clip1", 10.0)])

    def getClips(self):
        return self._clips

    @QtCore.Slot(int)
    def clicked(self, index):
        print "Python : start removing element at index %s" % index
        self._clips.removeAt(index)
        print "Python : end removing element at index %s" % index

    modelChanged = QtCore.Signal()
    clips = QtCore.Property("QVariant", getClips, notify=modelChanged)


def main():
    app = QtGui.QApplication(sys.argv)
    view = QtDeclarative.QDeclarativeView()

    mw = MainWrapper(view)
    view.rootContext().setContextProperty("_mainWrapper", mw)
    view.setSource("source.qml")
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)

    view.show()
    app.exec_()

if __name__ == '__main__':
    main()

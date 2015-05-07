import sys
sys.path.append("../..")

from quickmamba.models import QObjectListModel

from PyQt5 import QtCore, QtWidgets, QtQuick


class ClipWrapper(QtCore.QObject):
    def __init__(self, parent, name, duration):
        super(ClipWrapper, self).__init__(parent)
        self._name = name
        self._duration = duration

    def getName(self):
        return self._name

    def getDuration(self):
        return self._duration

    nameChanged = QtCore.pyqtSignal()
    durationChanged = QtCore.pyqtSignal()
    name = QtCore.pyqtProperty(str, getName, notify=nameChanged)
    duration = QtCore.pyqtProperty(int, getDuration, notify=durationChanged)


class MainWrapper(QtCore.QObject):
    def __init__(self, parent):
        super(MainWrapper, self).__init__(parent)
        self._clips = QObjectListModel(self)
        self._clips.setObjectList([ClipWrapper(parent, "Clip0", 2.2), ClipWrapper(parent, "Clip1", 10.0)])

    def getClips(self):
        return self._clips

    modelChanged = QtCore.pyqtSignal()
    clips = QtCore.pyqtProperty(QtCore.QObject, getClips, notify=modelChanged)


def main():
    app = QtWidgets.QApplication(sys.argv)
    view = QtQuick.QQuickView()

    mw = MainWrapper(view)
    view.rootContext().setContextProperty("_mainWrapper", mw)
    view.setSource(QtCore.QUrl("source.qml"))
    view.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)

    view.show()
    app.exec_()

if __name__ == '__main__':
    main()

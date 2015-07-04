import sys
sys.path.append("../..")

import logging

from quickmamba.models import QObjectListModel

from PyQt5 import QtCore, QtWidgets, QtQuick


class ClipWrapper(QtCore.QObject):
    def __init__(self, parent, name, duration):
        QtCore.QObject.__init__(self, parent)
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
        QtCore.QObject.__init__(self, parent)
        self._qtParent = parent
        self._clips = QObjectListModel(self)
        self._clips.setObjectList(
                [ClipWrapper(self._qtParent, "Clip0", 2.2),
                ClipWrapper(self._qtParent, "Clip1", 10.0),
                ClipWrapper(self._qtParent, "Clip1", 10.0),
                ClipWrapper(self._qtParent, "Clip1", 10.0),
                ClipWrapper(self._qtParent, "Clip1", 10.0)]
            )

    def getClips(self):
        return self._clips

    @QtCore.pyqtSlot(int)
    def remove(self, index):
        logging.debug("Python : start removing element at index %s" % index)
        self._clips.removeAt(index)
        logging.debug("Python : end removing element at index %s" % index)

    @QtCore.pyqtSlot()
    def add(self):
        logging.debug("Python : start adding element")
        self._clips.append(ClipWrapper(self._qtParent, "ClipDynamic", 2.2) )
        logging.debug("Python : end adding element")

    @QtCore.pyqtSlot(int)
    def insertAt(self, index):
        logging.debug("Python : start insertAt %s element" % index)
        self._clips.insert(index, ClipWrapper(self._qtParent, "ClipDynamic", 2.2) )
        logging.debug("Python : end insertAt element")

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

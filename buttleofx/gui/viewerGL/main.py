from glviewport import GLViewport

from PySide import QtGui, QtDeclarative, QtOpenGL

import os

currentFilePath = os.path.dirname(os.path.abspath(__file__))


def main(argv):
    # Launch a DeclarativeView
    app = QtGui.QApplication(argv)

    decView = QtDeclarative.QDeclarativeView()
    decView.setViewport( QtOpenGL.QGLWidget() )
    QtDeclarative.qmlRegisterType(GLViewport, "Viewport", 1, 0, "GLViewport")
    
    decView.setSource(os.path.join(currentFilePath, "Viewer.qml"))
    decView.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
    decView.setWindowTitle("Viewer OpenGL")
    decView.show()
    app.exec_()


from glviewport import GLViewport

from PySide import QtGui, QtDeclarative, QtOpenGL


def main():
    # Launch a DeclarativeView
    app = QtGui.QApplication("")

    decView = QtDeclarative.QDeclarativeView()

    decView.setViewport( QtOpenGL.QGLWidget() )

    QtDeclarative.qmlRegisterType(GLViewport, "Viewport", 1, 0, "GLViewport")
    decView.setSource("Viewer.qml")
    decView.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
    decView.setWindowTitle("Viewer OpenGL")
    decView.show()
    app.exec_()


if __name__ == '__main__':
    main()



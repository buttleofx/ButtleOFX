import os
import logging

from PyQt5 import QtCore, QtWidgets, QtQuick, QtQml, QtOpenGL

tuttleofx_installed = False
try:
    import pyTuttle  # noqa
    tuttleofx_installed = True
    logging.debug('Use TuttleOFX.')
except:
    logging.debug('TuttleFX not installed, use Python Image Library instead.')
if tuttleofx_installed:
    from glviewport_tuttleofx import GLViewport_tuttleofx
else:
    from glviewport_pil import GLViewport_pil


currentFilePath = os.path.dirname(os.path.abspath(__file__))


class ButtleApp(QtWidgets.QApplication):
    def __init__(self, argv):
        super(ButtleApp, self).__init__(argv)

    def notify(self, receiver, event):
        try:
            # logging.debug("QApp notify")
            return QtWidgets.QApplication.notify(self, receiver, event)
        except Exception as e:
            logging.warning("QApp notify exception: " + str(e))
            import traceback
            traceback.print_exc()
            return False


def main(argv):
    # Launch a QuickView
    app = ButtleApp(argv)

    decView = QtQuick.QQuickView()
    decView.setViewport(QtOpenGL.QGLWidget())
    decView.setViewportUpdateMode(QtQuick.QQuickView.FullViewportUpdate)

    if tuttleofx_installed:
        QtQml.qmlRegisterType(GLViewport_tuttleofx, "Viewport", 1, 0, "GLViewport")
    else:
        QtQml.qmlRegisterType(GLViewport_pil, "Viewport", 1, 0, "GLViewport")

    decView.setSource(QtCore.QUrl(os.path.join(currentFilePath, "Viewer.qml")))
    decView.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)
    decView.setWindowTitle("Viewer OpenGL")
    decView.show()
    app.exec_()

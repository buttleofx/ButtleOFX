tuttleofx_installed = False
try:
    import pyTuttle
    tuttleofx_installed = True
    print('Use TuttleOFX.')
except:
    print('TuttleFX not installed, use Python Image Library instead.')

if tuttleofx_installed:
    from glviewport_tuttleofx import GLViewport_tuttleofx
else:
    from glviewport_pil import GLViewport_pil


from PySide import QtGui, QtDeclarative, QtOpenGL

import os

currentFilePath = os.path.dirname(os.path.abspath(__file__))

class ButtleApp(QtGui.QApplication):
    def __init__(self, argv):
        super(ButtleApp, self).__init__(argv)
    
    def notify(self, receiver, event):
        try:
            #print("QApp notify")
            return QtGui.QApplication.notify(self, receiver, event)
        except Exception as e:
            print("QApp notify exception: " + str(e))

def main(argv):
    # Launch a DeclarativeView
    app = ButtleApp(argv)

    decView = QtDeclarative.QDeclarativeView()
    decView.setViewport( QtOpenGL.QGLWidget() )
    if tuttleofx_installed:
        QtDeclarative.qmlRegisterType(GLViewport_tuttleofx, "Viewport", 1, 0, "GLViewport")
    else:
        QtDeclarative.qmlRegisterType(GLViewport_pil, "Viewport", 1, 0, "GLViewport")
    
    decView.setSource(os.path.join(currentFilePath, "Viewer.qml"))
    decView.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
    decView.setWindowTitle("Viewer OpenGL")
    decView.show()
    app.exec_()


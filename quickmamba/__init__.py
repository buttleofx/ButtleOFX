import os

currentFilePath = os.path.dirname(os.path.abspath(__file__))


def qmlRegister():
    print("-"*50)
    pathlist = os.getenv("QML_IMPORT_PATH", "").split(os.pathsep)
    os.environ["QML_IMPORT_PATH"] = os.pathsep.join(pathlist + [os.path.join(currentFilePath, "../qml")])
    os.environ["QML2_IMPORT_PATH"] = os.pathsep.join(pathlist + [os.path.join(currentFilePath, "../qml")])

    print("QML_IMPORT_PATH:", os.environ["QML_IMPORT_PATH"])
    import quickmamba.gui
    quickmamba.gui.qmlRegister()



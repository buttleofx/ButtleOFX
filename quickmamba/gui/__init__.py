from wheelArea import WheelArea

from PySide import QtDeclarative

def qmlRegister():
    QtDeclarative.qmlRegisterType(WheelArea, "QuickMamba", 1, 0, "WheelAreaImpl")



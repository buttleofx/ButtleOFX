from wheelArea import WheelArea
from dropArea import DropArea

from PySide import QtDeclarative

def qmlRegister():
    QtDeclarative.qmlRegisterType(WheelArea, "QuickMamba", 1, 0, "WheelAreaImpl")
    QtDeclarative.qmlRegisterType(DropArea, "QuickMamba", 1, 0, "DropAreaImpl")



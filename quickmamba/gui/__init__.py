from .wheelArea import WheelArea
from .externDropArea import ExternDropArea
from .colorExtended import ColorExtended
from .colorPicker import ColorPicker

from PyQt5 import QtQml

def qmlRegister():
    QtQml.qmlRegisterType(WheelArea, "QuickMamba", 1, 0, "WheelAreaImpl")
    QtQml.qmlRegisterType(ExternDropArea, "QuickMamba", 1, 0, "ExternDropAreaImpl")
    QtQml.qmlRegisterType(ColorExtended, "QuickMamba", 1, 0, "ColorExtended")
    QtQml.qmlRegisterType(ColorPicker, "QuickMamba", 1, 0, "ColorPicker")


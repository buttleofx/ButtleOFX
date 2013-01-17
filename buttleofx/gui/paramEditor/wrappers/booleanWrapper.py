from PySide import QtCore


class BooleanWrapper(QtCore.QObject):
    def __init__(self, paramElmt):
        QtCore.QObject.__init__(self)
        self._paramType = paramElmt.paramType
        self._text = paramElmt.text
        self._defaultValue = paramElmt.defaultValue

    #################### getters ####################

    def getParamType(self):
        return self._paramType

    def getText(self):
        return self._text

    def getDefaultValue(self):
        return self._defaultValue

    #################### setters ####################

    def setParamType(self, paramType):
        self._paramType = paramType

    def setText(self, text):
        self._text = text

    def setDefaultValue(self, defaultValue):
        self._defaultValue = defaultValue

    # Just temporary : paramType must be constant
    changed = QtCore.Signal()

    paramType = QtCore.Property(unicode, getParamType, setParamType, notify=changed)
    text = QtCore.Property(unicode, getText, setText, notify=changed)
    defaultValue = QtCore.Property(bool, getDefaultValue, setDefaultValue, notify=changed)

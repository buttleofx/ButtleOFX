from PySide import QtCore


class RGBAWrapper(QtCore.QObject):
    """
        Gui class, which maps a ParamRGBA.
    """

    def __init__(self, param):
        QtCore.QObject.__init__(self)
        self._param = param
        self._param.changed.connect(self.emitChanged)

    #################### getters ####################

    def getParamType(self):
        return self._param.getParamType()

    def getDefaultR(self):
        return self._param.getDefaultR()

    def getDefaultG(self):
        return self._param.getDefaultG()

    def getDefaultB(self):
        return self._param.getDefaultB()

    def getDefaultA(self):
        return self._param.getDefaultA()

    def getValue(self):
        return self._param.getValue()

    def getValueR(self):
        return self._param.getValueR()

    def getValueG(self):
        return self._param.getValueG()

    def getValueB(self):
        return self._param.getValueB()

    def getValueA(self):
        return self._param.getValueA()

    def getText(self):
        return self._param.getText()

    #################### setters ####################

    def setValue(self, values):
        self._param.setValue(values)

    def setValueR(self, value):
        self._param.setValueR(value)

    def setValueG(self, value):
        self._param.setValueG(value)

    def setValueB(self, value):
        self._param.setValueB(value)

    def setValueA(self, value):
        self._param.setValueA(value)

    def setText(self, text):
        self._param.setText(text)

    @QtCore.Signal
    def changed(self):
        pass

    def emitChanged(self):
        self.changed.emit()

    ################################################## DATA EXPOSED TO QML ##################################################

    paramType = QtCore.Property(unicode, getParamType, notify=changed)
    text = QtCore.Property(unicode, getText, setText, notify=changed)
    r = QtCore.Property(int, getValueR, setValueR, notify=changed)
    g = QtCore.Property(int, getValueG, setValueG, notify=changed)
    b = QtCore.Property(int, getValueB, setValueB, notify=changed)
    a = QtCore.Property(int, getValueA, setValueA, notify=changed)

from PySide import QtCore


class RGBWrapper(QtCore.QObject):
    """
        Gui class, which maps a ParamRGB.
    """

    def __init__(self, param):
        QtCore.QObject.__init__(self)
        self._param = param
        self._param.paramChanged.connect(self.emitChanged)

    #################### getters ####################

    def getParamType(self):
        return self._param.getParamType()

    def getDefaultR(self):
        return self._param.getDefaultR()

    def getDefaultG(self):
        return self._param.getDefaultG()

    def getDefaultB(self):
        return self._param.getDefaultB()

    def getValue(self):
        return self._param.getValue()

    def getValueR(self):
        return self._param.getValueR()

    def getValueG(self):
        return self._param.getValueG()

    def getValueB(self):
        return self._param.getValueB()

    def getText(self):
        return self._param.getText()
        
    def isSecret(self):
        return self._param.isSecret()

    #################### setters ####################

    def setValue(self, values):
        self._param.setValue(values)

    def setValueR(self, value):
        self._param.setValueR(value)

    def setValueG(self, value):
        self._param.setValueG(value)

    def setValueB(self, value):
        self._param.setValueB(value)

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
    r = QtCore.Property(float, getValueR, setValueR, notify=changed)
    g = QtCore.Property(float, getValueG, setValueG, notify=changed)
    b = QtCore.Property(float, getValueB, setValueB, notify=changed)

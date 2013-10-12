from .paramWrapper import ParamWrapper

from PySide import QtCore


class RGBWrapper(ParamWrapper):
    """
        Gui class, which maps a ParamRGB.
    """

    def __init__(self, param):
        ParamWrapper.__init__(self, param)

    #################### getters ####################

    def getDefaultR(self):
        return self._param.getDefaultR()

    def getDefaultG(self):
        return self._param.getDefaultG()

    def getDefaultB(self):
        return self._param.getDefaultB()

    def getValueR(self):
        return self._param.getValueR()

    def getValueG(self):
        return self._param.getValueG()

    def getValueB(self):
        return self._param.getValueB()

    #################### setters ####################

    def setValueR(self, value):
        self._param.setValueR(value)

    def setValueG(self, value):
        self._param.setValueG(value)

    def setValueB(self, value):
        self._param.setValueB(value)

    @QtCore.Signal
    def changed(self):
        pass

    ################################################## DATA EXPOSED TO QML ##################################################

    r = QtCore.Property(float, getValueR, setValueR, notify=changed)
    g = QtCore.Property(float, getValueG, setValueG, notify=changed)
    b = QtCore.Property(float, getValueB, setValueB, notify=changed)

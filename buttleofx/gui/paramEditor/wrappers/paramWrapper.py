from PySide import QtCore

class ParamWrapper(object):
    """
        Define the common methods and fields for paramsWrappers.
    """
    def __init__(self, param):

        self._param = param
        self._param.changed.connect(self.emitChanged)

    def isSecret(self):
        return self._param.isSecret()



   
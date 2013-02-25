# quickmamba
from quickmamba.patterns import Signal


class Param:
    """
    Define the common methods and fields for all params.
    Containts field :
        - changed : signal emitted when we set value(s) of the param.
    """
    def __init__(self):
        self.changed = Signal()
        self._hasChanged = False

    def isSecret(self):
        return self._tuttleParam.getSecret()

    def getHasChanged(self):
        return self._hasChanged

    def setHasChanged(self, changed):
        self._hasChanged = changed

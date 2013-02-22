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

    def isSecret(self):
        return self._tuttleParam.getSecret()
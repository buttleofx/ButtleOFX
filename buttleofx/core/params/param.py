# quickmamba
from quickmamba.patterns import Signal


class Param:
    """
    Define the common methods and fields for all params.
    Containts field :
        - _tuttleParam : the tuttle Param.
        - _paramChanged : signal emitted when we set value(s) of the param.
    """
    def __init__(self, tuttleParam):
        # the tuttle param
        self._tuttleParam = tuttleParam

        # signal
        self.paramChanged = Signal()

    #################### getters ####################

    def getTuttleParam(self):
        return self._tuttleParam

    def getText(self):
        return self._tuttleParam.getName()[0].capitalize() + self._tuttleParam.getName()[1:]

    def isSecret(self):
        return self._tuttleParam.getSecret()


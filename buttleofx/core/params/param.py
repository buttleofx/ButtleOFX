from quickmamba.patterns import Signal


class Param:
    """
    Define the common methods and fields for all params.
    Containts field :
        - _tuttleParam : the tuttle Param.
        - _paramChanged : signal emitted when we set value(s) of the param.
    """

    def __init__(self, tuttleParam):
        # The tuttle param
        self._tuttleParam = tuttleParam

        # Signal
        self.paramChanged = Signal()

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getDefaultValue(self):
        """
            Virtual function.
            Returns the default value(s) of the param.
        """
        raise NotImplementedError()

    def getName(self):
        return self._tuttleParam.getName()

    def getParamDoc(self):
        """
            Virtual function.
            Returns the doc of the param.
        """
        raise NotImplementedError()

    def getParamType(self):
        """
            Virtual function.
            Returns the type of the param.
        """
        raise NotImplementedError()

    def getText(self):
        """
            Same as getName, but with the first letter in capital.
        """
        return self._tuttleParam.getLabel()

    def getTuttleParam(self):
        return self._tuttleParam

    def getValue(self):
        """
            Virtual function.
            Returns the value(s) of the param.
        """
        raise NotImplementedError()

    def setValue(self, values):
        """
            Virtual function.
            Set the tuttle value(s) of the param (but do not push a command in the CommandManager.
        """
        raise NotImplementedError()

    # ## Others ## #

    def dict_to_object(self, paramData):
        """
            Set all values of the param, from a dictionary.
        """
        self.setValue(paramData["value"])

    def isSecret(self):
        return self._tuttleParam.getSecret()

    def object_to_dict(self):
        """
            Convert the param to a dictionary of his representation.
            We do not save param which had not been changed.
        """
        if self.getValue() == self.getDefaultValue():
            return None
        param = {
            "name": self.getName(),
            "value": self.getValue()
        }
        return param

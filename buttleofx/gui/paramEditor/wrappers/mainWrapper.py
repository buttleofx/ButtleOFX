from buttleofx.gui.paramEditor.params import ParamInt
from buttleofx.gui.paramEditor.params import ParamString
from buttleofx.gui.paramEditor.params import ParamBoolean
from buttleofx.gui.paramEditor.params import ParamDouble
from buttleofx.gui.paramEditor.params import ParamDouble2D
from buttleofx.gui.paramEditor.params import ParamDouble3D

from buttleofx.gui.paramEditor.wrappers import IntWrapper
from buttleofx.gui.paramEditor.wrappers import StringWrapper
from buttleofx.gui.paramEditor.wrappers import BooleanWrapper
from buttleofx.gui.paramEditor.wrappers import DoubleWrapper
from buttleofx.gui.paramEditor.wrappers import Double2DWrapper
from buttleofx.gui.paramEditor.wrappers import Double3DWrapper

from quickmamba.models import QObjectListModel

from PySide import QtCore


class MainWrapper(QtCore.QObject):
    def __init__(self, parent, paramList):
        super(MainWrapper, self).__init__(parent)
        #QtCore.QObject.__init__(self)
        self._paramElmts = QObjectListModel(self)

        mapTypeToWrapper = {
            ParamInt: IntWrapper,
            ParamString: StringWrapper,
            ParamDouble: DoubleWrapper,
            ParamDouble2D: Double2DWrapper,
            ParamDouble3D: Double3DWrapper,
            ParamBoolean: BooleanWrapper
        }

        paramListModel = [mapTypeToWrapper[paramElt.__class__](paramElt) for paramElt in paramList]
        self._paramElmts.setObjectList(paramListModel)

    def getParamElts(self):
        return self._paramElmts

    modelChanged = QtCore.Signal()
    paramElmts = QtCore.Property("QVariant", getParamElts, notify=modelChanged)

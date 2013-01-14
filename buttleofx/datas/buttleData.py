from buttleofx.gui.graph import Graph
from buttleofx.gui.graph import GraphWrapper

from quickmamba.patterns import Singleton

class ButtleData(Singleton):
    """
        Class ButtleData defined by:
        - _graph
        - _graphWrapper

        This class containts all data we need to manage the application.
        Emit signal when modifications happen
    """
    
    def getGraph(self):
        return self._graph

    def setGraph(self, graph):
        self._graph = graph

    def getGraphWrapper(self):
        return self._graphWrapper

    def setGraphWrapper(self, graphWrapper):
        self._graphWrapper = graphWrapper

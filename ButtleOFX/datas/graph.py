from gui.graph.nodeManager import NodeManager
from quickmamba.patterns import Singleton

class Graph(Singleton) :

    """
        Class GraphData defined by:
        - coreNode list
        - connexions
    """

    def __init__(self, coreNodes):
        self.coreNodes = coreNodes
        # self.connexions = connexions
from datas.graphData import GraphData
from quickmamba.patterns import Singleton

class ButtleData(Singleton) :

	"""
        Class ButtleData defined by:
        - graph
        - nodeWrapper List
        - nodeItem List (QML object)

        Emit signal when modifications happen
    """

    def __init__(self, graph, nodeWrappers, nodeItems):
        self.graph = graph
        self.nodeWrappers = nodeWrappers
        self.nodeItems = nodeItems

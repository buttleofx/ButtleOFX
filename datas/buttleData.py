from datas.graphData import GraphData

class ButtleData(QtCore.QObject) :

	"""
        Class ButtleData defined by:
        - graph
        - nodeWrapper List
        - nodeItem List (QML object)

        Emit signal when modifications happen

        One object of this class => singleton
    """

    def __init__(self, graph, nodeWrappers, nodeItems):
        self.graph = graph
        self.nodeWrappers = nodeWrappers
        self.nodeItems = nodeItems

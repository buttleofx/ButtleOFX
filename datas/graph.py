from gui.graph.nodeManager import NodeManager

class Graph(QtCore.QObject) :

    """
        Class GraphData defined by:
        - coreNode list
        - connexions


        One object of this class => singleton
    """

    def __init__(self, coreNodes):
    # def __init__(self, coreNodes, connexions):
        self.coreNodes = coreNodes
        # self.connexions = connexions
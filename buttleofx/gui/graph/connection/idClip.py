class IdClip:
    """
        Class usefull to identify a clip with :
        - the graph
        - the node ID
        - the port (input or output)
        - the clip number
    """

    def __init__(self, node, port, clipNumber):
        #self._graph = graph
        self._node = node
        self._port = port
        self._clipNumber = clipNumber

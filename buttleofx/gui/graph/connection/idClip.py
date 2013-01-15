class IdClip:
    """
        Class usefull to identify a clip with :
        - the graph
        - the node name
        - the port (input or output)
        - the clip number
    """

    def __init__(self, nodeName, port, clipNumber, coord):
        #self._graph = graph
        self._nodeName = nodeName
        self._port = port
        self._clipNumber = clipNumber

        self._coord = coord

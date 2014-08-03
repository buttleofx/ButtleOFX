import logging
from pyTuttle import tuttle
from PyQt5 import QtCore
from quickmamba.patterns import Signal
from buttleofx.data import ButtleDataSingleton


class ViewerManager(QtCore.QObject):
    """
        This class manages actions about the viewer.
    """

    def __init__(self):
        super(ViewerManager, self).__init__()

        self._tuttleImageCache = None
        self._computedImage = None
        self._videoIsPlaying = False

        # For the viewer : name of the hypothetical node that can't be displayed.
        self._nodeError = ""

        self.undoRedoChanged = Signal()

    # ############################################ Methods exposed to QML ############################################ #

    # QtCore.pyqtSlot()
    # ef mosquitoDragEvent(self):
    #    """
    #     Function called when the viewer's mosquito is dragged.
    #     The function sends the mimeData and launches a drag event.
    # """
    #
    #    widget = QtGui.QWidget()
    #    drag = QtGui.QDrag(widget)
    #    mimeData = QtCore.QMimeData()
    #
    #    # set data (here it's just a text)
    #    mimeData.setText("mosquito_of_the_dead")
    #    drag.setMimeData(mimeData)
    #
    #    # sets the image of the mosquito in the pixmap
    #    filePath = ButtleDataSingleton().get().getButtlePath()
    #    imgPath = filePath + "/gui/img/mosquito/mosquito.png"
    #    drag.setPixmap(QtGui.QPixmap(imgPath))
    #
    #    # starts the drag
    #    drag.exec_(QtCore.Qt.MoveAction)

    # ######################################## Methods private to this class ####################################### #

    # ## Getters ## #

    def getNodeError(self):
        """
            Returns the name of the node that can't be displayed.
        """
        return self._nodeError

    # ## Setters ## #

    def setNodeError(self, nodeName):
        """
            Sets the name of the node that can't be displayed.
            Emit signal which is displayed on the viewer.
        """
        self._nodeError = nodeName
        self.nodeErrorChanged.emit()

    # ## Others ## #

    def computeNode(self, node, frame):
        """
            Computes the node (displayed in the viewer) at the frame indicated.
        """
        buttleData = ButtleDataSingleton().get()
        graphTuttle = buttleData.getCurrentGraph().getGraphTuttle()

        # Get the output where we save the result
        self._tuttleImageCache = tuttle.MemoryCache()

        if buttleData.getVideoIsPlaying():  # If a video is playing
            processGraph = buttleData.getProcessGraph()
            processGraph.setupAtTime(frame)
            processGraph.processAtTime(self._tuttleImageCache, frame)
        else:  # If it's an image only
            processOptions = tuttle.ComputeOptions(int(frame))
            logging.debug("computeNode: Start compute - frame: {0}, node: {1}".format(frame, node))
            processGraph = tuttle.ProcessGraph(processOptions, graphTuttle, [node], tuttle.core().getMemoryCache())
            processGraph.setup()
            timeRange = tuttle.TimeRange(frame, frame, 1)  # buttleData.getTimeRange()
            processGraph.beginSequence(timeRange)
            processGraph.setupAtTime(frame)
            processGraph.processAtTime(self._tuttleImageCache, frame)
            processGraph.endSequence()
            logging.debug("computeNode: End tuttle computation.")

        self._computedImage = self._tuttleImageCache.get(0)

        # Add the computedImage to the map
        hashMap = tuttle.NodeHashContainer()
        graphTuttle.computeGlobalHashAtTime(hashMap, frame, [node])
        hasCode = hashMap.getHash(node, frame)

        # Max 15 computedImages saved in memory
        if (hasCode not in buttleData._mapNodeNameToComputedImage.keys() and
                len(buttleData._mapNodeNameToComputedImage) < 15):
            buttleData._mapNodeNameToComputedImage.update({hasCode: self._computedImage})
        elif (hasCode not in buttleData._mapNodeNameToComputedImage.keys() and
                len(buttleData._mapNodeNameToComputedImage) >= 15):
            # Delete a computed image from the memory (random)
            buttleData._mapNodeNameToComputedImage.popitem()
            buttleData._mapNodeNameToComputedImage.update({hasCode: self._computedImage})

        return self._computedImage

    def retrieveImage(self, frame, frameChanged):
        """
            Computes the node at the frame indicated if the frame has changed (if the time has changed).
        """
        buttleData = ButtleDataSingleton().get()
        # Get the name of the currentNode of the viewer
        node = buttleData.getCurrentViewerNodeName()

        try:
            # Get the global node hash ID
            if node is not None:
                hashMap = tuttle.NodeHashContainer()
                buttleData.getCurrentGraph().getGraphTuttle().computeGlobalHashAtTime(hashMap, frame, [node])
                node_hashCode = hashMap.getHash(node, frame)
            # Get the buttle latest images map
            mapNodeToImage = buttleData.getMapNodeNameToComputedImage()

            self.setNodeError("")
            for key in mapNodeToImage.keys():
                # If the image is already calculated
                if node_hashCode == key and frameChanged is False:
                    # print("**************************Image already calculated**********************")
                    return mapNodeToImage.get(node_hashCode)
            # If it is not
            # print("**************************Image is not already calculated**********************")
            return self.computeNode(node, frame)
        except Exception as e:
            logging.debug("Can't display node : " + node)
            self.setNodeError(str(e))
            raise

    # ############################################# Data exposed to QML ############################################## #

    # Error displayed on the Viewer
    nodeErrorChanged = QtCore.pyqtSignal()
    nodeError = QtCore.pyqtProperty(str, getNodeError, setNodeError, notify=nodeErrorChanged)

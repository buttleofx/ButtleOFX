from PySide import QtCore, QtGui
# quickmamba
from quickmamba.patterns import Signal
# Tuttle
from pyTuttle import tuttle
# data
from buttleofx.data import ButtleDataSingleton


class ViewerManager(QtCore.QObject):
    """
        This class manages actions about the viewer.
    """

    def __init__(self):
        super(ViewerManager, self).__init__()

        self._tuttleImageCache = None
        self._computedImage = None

        # for the viewer : name of the hypothetical node that can't be displayed.
        self._nodeError = ""

        self.undoRedoChanged = Signal()

    def getNodeError(self):
        """
            Returns the name of the node that can't be displayed.
        """
        return self._nodeError

    def setNodeError(self, nodeName):
        """
            Sets the name of the node that can't be displayed.
            Emit signal which is displayed on the viewer. 
        """
        self._nodeError = nodeName
        self.nodeErrorChanged.emit()

    def computeNode(self, frame):
        """
            Computes the node at the frame indicated.
        """
        #print "------- COMPUTE NODE -------"

        buttleData = ButtleDataSingleton().get()
        #Get the name of the currentNode of the viewer
        node = buttleData.getCurrentViewerNodeName()
        #Get the output where we save the result
        self._tuttleImageCache = tuttle.MemoryCache()
        #compute the image at the frame given in argument
        buttleData.getGraph().getGraphTuttle().compute(self._tuttleImageCache, node, tuttle.ComputeOptions(int(frame)))

        self._computedImage = self._tuttleImageCache.get(0)

        #Add the computedImage to the map
        buttleData._mapNodeNameToComputedImage.update({node: self._computedImage})

        return self._computedImage

    def retrieveImage(self, frame, frameChanged):
        """
            Computes the node at the frame indicated if the frame has changed (if the time has changed).
        """
        buttleData = ButtleDataSingleton().get()
        #Get the name of the currentNode of the viewer
        node = buttleData.getCurrentViewerNodeName()
        #Get the map
        mapNodeToImage = buttleData.getMapNodeNameToComputedImage()

        try:
            self.setNodeError("")
            #If the image is already calculated
            for element in mapNodeToImage:
                if node == element and frameChanged is False:
                    print "**************************Image already calculated**********************"
                    return buttleData._mapNodeNameToComputedImage[node]
                # If it is not
            #print "************************Calcul of image***************************"
            return self.computeNode(frame)
        except Exception as e:
            print "Can't display node : " + node
            self.setNodeError(str(e))
            raise

    @QtCore.Slot()
    def mosquitoDragEvent(self):
        """
            Function called when the viewer's mosquito is dragged.
            The function sends the mimeData and launches a drag event.
        """

        widget = QtGui.QWidget()
        drag = QtGui.QDrag(widget)
        mimeData = QtCore.QMimeData()

        # set data (here it's just a text)
        mimeData.setText("mosquito_of_the_dead")
        drag.setMimeData(mimeData)

        # sets the image of the mosquito in the pixmap
        filePath = ButtleDataSingleton().get().getButtlePath()
        imgPath = filePath + "/gui/img/mosquito/mosquito.png"
        drag.setPixmap(QtGui.QPixmap(imgPath))

        # starts the drag
        drag.exec_(QtCore.Qt.MoveAction)

    # error displayed on the Viewer
    nodeErrorChanged = QtCore.Signal()
    nodeError = QtCore.Property(str, getNodeError, setNodeError, notify=nodeErrorChanged)

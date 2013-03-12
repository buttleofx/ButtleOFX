from PySide import QtCore, QtGui
import os
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

        # for the viewer
        self._nodeError = ""

        self.undoRedoChanged = Signal()

    def getNodeError(self):
        """
            Returns the name of the node that can't be displayed.
        """
        return self._nodeError

    def setNodeError(self, nodeName):
        self._nodeError = nodeName
        self.nodeErrorChanged.emit()

    def computeNode(self, frame):
        """
            Compute the node at the frame indicated
        """
        print "------- COMPUTE NODE -------"

        buttleData = ButtleDataSingleton().get()
        #Get the name of the currentNode of the viewer
        node = buttleData.getCurrentViewerNodeName()

        #Get the output where we save the result
        self._tuttleImageCache = tuttle.MemoryCache()
        #should replace 25 by the fps of the video (a sort of getFPS(node))
        #should expose the duration of the video to the QML too
        buttleData.getGraph().getGraphTuttle().compute(self._tuttleImageCache, node, tuttle.ComputeOptions(int(frame)))
        self._computedImage = self._tuttleImageCache.get(0)

        #Add the computedImage to the map
        buttleData._mapNodeNameToComputedImage.update({node: self._computedImage})

        return self._computedImage

    def retrieveImage(self, frame, frameChanged):
        """
            Compute the node at the frame indicated if the frame has changed (if the time has changed)
        """
        buttleData = ButtleDataSingleton().get()
        #Get the name of the currentNode of the viewer
        node = buttleData.getCurrentViewerNodeName()
        #Get the map
        mapNodeToImage = buttleData._mapNodeNameToComputedImage

        try:
            self.setNodeError("")
            #If the image is already calculated
            for element in mapNodeToImage:
                if node == element and frameChanged is False:
                    print "**************************Image already calculated**********************"
                    return buttleData._mapNodeNameToComputedImage[node]
                # If it is not
            print "************************Calcul of image***************************"
            return self.computeNode(frame)
        except Exception as e:
            print "Can't display node : " + node
            buttleData.setNodeError(str(e))
            raise

    @QtCore.Slot()
    def mosquitoDragEvent(self):
        """
            Function called when the viewer's mosquito is dragged.
            The function send the mimeData and launch a drag event.
        """

        widget = QtGui.QWidget()
        drag = QtGui.QDrag(widget)

        mimeData = QtCore.QMimeData()
        mimeData.setText("mosquito_of_the_dead")
        drag.setMimeData(mimeData)

        filePath = ButtleDataSingleton().get().getButtlePath()
        imgPath = filePath + "/gui/img/mosquito/mosquito.png"
        drag.setPixmap(QtGui.QPixmap(imgPath))

        drag.exec_(QtCore.Qt.MoveAction)

    # error display on the Viewer
    nodeErrorChanged = QtCore.Signal()
    nodeError = QtCore.Property(str, getNodeError, setNodeError, notify=nodeErrorChanged)

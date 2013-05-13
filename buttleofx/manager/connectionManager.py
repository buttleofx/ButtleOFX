from PySide import QtCore, QtGui
# quickmamba
from quickmamba.patterns import Signal
# data
from buttleofx.data import ButtleDataSingleton
# connection
from buttleofx.core.graph.connection import IdClip


class ConnectionManager(QtCore.QObject):
    """
        This class manages actions about connections.
    """

    def __init__(self):
        super(ConnectionManager, self).__init__()

        self.undoRedoChanged = Signal()

    ############### flags ###############

    def canConnect(self, clip1, clip2):
        """
            Returns True if the connection between the nodes is possible, else False.
            A connection is possible if the clip isn't already taken, and if the clips are from 2 different nodes, not already connected.
        """
        buttleData = ButtleDataSingleton().get()
        graph = buttleData.getGraph()

        # if the clips are from the same node : False
        if (clip1.getNodeName() == clip2.getNodeName()):
            return False

        # if the clips are 2 inputs or 2 outputs : False
        if (clip1.getClipName() == "Output" and clip2.getClipName() == "Output") or (clip1.getClipName() != "Output" and clip2.getClipName() != "Output"):
            return False

        # if the input clip is already taken : False
        if (clip1.getClipName() != "Output" and graph.contains(clip1)) or (clip2.getClipName() != "Output" and graph.contains(clip2)):
            return False

        # if the nodes containing the clips are already connected : False
        if(graph.nodesConnected(clip2, clip1)):
            return False

        return True

    @QtCore.Slot(str, QtCore.QObject, int, result=bool)
    def canConnectTmpNodes(self, dataTmpClip, clip, clipIndex):
        """
            Returns True if the connection between the nodes is possible, else False.
            This function is called by Clip.qml on the event onDragEnter, to display in real time if the nodes can be connected (during a creation of a connection).
            It simulates a connection and calls the function self.canConnect(clip1, clip2).
        """
        buttleData = ButtleDataSingleton().get()

        # we split the data of the tmpClip (from mimeData) to find needed informations about this clip.
        infosTmpClip = dataTmpClip.split("/")

        if infosTmpClip[0] != "clip" or len(infosTmpClip) != 4:
            return False
        else:
            tmpClipNodeName, tmpClipName, tmpClipIndex = infosTmpClip[1], infosTmpClip[2], int(infosTmpClip[3])

        # we find the position of this tmpClip to be able to create a IdClip object.
        positionTmpClip = buttleData.getGraphWrapper().getPositionClip(tmpClipNodeName, tmpClipName, tmpClipIndex)
        tmpClip = IdClip(tmpClipNodeName, tmpClipName, clipIndex, positionTmpClip)

        if tmpClip:
            # idem, for the "dropped" clip = newClip
            positionNewClip = buttleData.getGraphWrapper().getPositionClip(clip.getNodeName(), clip.getClipName(), clipIndex)
            newClip = IdClip(clip.getNodeName(), clip.getClipName(), clipIndex, positionNewClip)

            # finally we return if the clips can be connected
            return self.canConnect(tmpClip, newClip)

        else:
            return False

    ############### EVENTS FROM QML ###############

    @QtCore.Slot(QtCore.QObject, int)
    def connectionDragEvent(self, clip, clipIndex):
        """
            Function called when a clip is pressed (but not released yet).
            The function sends mimeData to identify the clip.
        """
        widget = QtGui.QWidget()
        drag = QtGui.QDrag(widget)
        mimeData = QtCore.QMimeData()

        # Sets informations of the first clip to the mimedata, as text.
        # Example of mimeData : "clip/TuttleJpegReader_1/Output/1"
        mimeData.setText("clip/" + str(clip.getNodeName()) + "/" + str(clip.getClipName()) + "/" + str(clipIndex))
        drag.setMimeData(mimeData)

        # transparent pixmap
        pixmap = QtGui.QPixmap(1, 1)
        pixmap.fill(QtCore.Qt.transparent)
        drag.setPixmap(pixmap)

        # starts the drag
        drag.exec_(QtCore.Qt.MoveAction)

    @QtCore.Slot(str, QtCore.QObject, int)
    def connectionDropEvent(self, dataTmpClip, clip, clipIndex):
        """
            Creates or deletes a connection between 2 clips ('tmpClip', the "dragged" clip, and 'newClip', the "dropped" clip)
            Arguments :
            - dataTmpClip : the string from mimeData, identifying the tmpClip (the "dragged" clip).
            - clip : the ClipWrapper of the "dropped" clip.
            - clipIndex : the index of the "dropped" clip.
        """
        buttleData = ButtleDataSingleton().get()

        # we split the data of the tmpClip (from mimeData) to find needed informations about this clip.
        infosTmpClip = dataTmpClip.split("/")

        if infosTmpClip[0] != "clip" or len(infosTmpClip) != 4:
            return  # use exception !
        else:
            tmpClipNodeName, tmpClipName, tmpClipIndex = infosTmpClip[1], infosTmpClip[2], int(infosTmpClip[3])

        # we find the position of this tmpClip to be able to create a IdClip object.
        positionTmpClip = buttleData.getGraphWrapper().getPositionClip(tmpClipNodeName, tmpClipName, tmpClipIndex)
        tmpClip = IdClip(tmpClipNodeName, tmpClipName, clipIndex, positionTmpClip)

        if tmpClip:
            # idem, for the "dropped" clip = newClip
            positionNewClip = buttleData.getGraphWrapper().getPositionClip(clip.getNodeName(), clip.getClipName(), clipIndex)
            newClip = IdClip(clip.getNodeName(), clip.getClipName(), clipIndex, positionNewClip)

            # a connection must be created from the ouput clip to the input clip (the order of the arguments is important !)
            if tmpClip.getClipName() == "Output":
                clipOut, clipIn = tmpClip, newClip
            else:
                clipOut, clipIn = newClip, tmpClip

            # if the clips can be connected, we connect them
            if self.canConnect(clipOut, clipIn):
                self.connect(clipOut, clipIn)
                return

            # else if they can't be connected, we check if they are already connected, and disconnect them if it is the case.
            else:
                connection = buttleData.getGraph().getConnectionByClips(clipOut, clipIn)
                if connection:
                    self.disconnect(buttleData.getGraphWrapper().getConnectionWrapper(connection.getId()))
                    return

        # update undo/redo display
        self.undoRedoChanged()

    ############### CREATION AND DESTRUCTION ###############

    def connect(self, clipOut, clipIn):
        """
            Adds a connection between 2 clips.
        """
        buttleData = ButtleDataSingleton().get()
        buttleData.getGraph().createConnection(clipOut, clipIn)

    @QtCore.Slot(QtCore.QObject)
    def disconnect(self, connectionWrapper):
        """
            Removes a connection between 2 clips.
        """
        buttleData = ButtleDataSingleton().get()
        buttleData.getGraph().deleteConnection(connectionWrapper.getConnection())

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


    @QtCore.Slot(QtCore.QObject, int)
    def connectionDragEvent(self, clip, clipNumber):
        """
            Function called when a clip is pressed (but not released yet).
            The function send mimeData to identify the clip.
        """
        mimeData = QtCore.QMimeData()
        mimeData.setText("clip/" + str(clip.getNodeName()) + "/" + str(clip.getName()) + "/" + str(clipNumber))

        widget = QtGui.QWidget()

        drag = QtGui.QDrag(widget)
        drag.setMimeData(mimeData)

        drag.exec_(QtCore.Qt.MoveAction)

    @QtCore.Slot(str, QtCore.QObject, int)
    def connectionDropEvent(self, dataTmpClip, clip, clipNumber):
        """
            Create or delete a connection between 2 nodes.
        """
        buttleData = ButtleDataSingleton().get()

        infosTmpClip = dataTmpClip.split("/")

        if infosTmpClip[0] != "clip" or len(infosTmpClip) != 4:
            return
        else:
            tmpClipNodeName, tmpClipName, tmpClipNumber = infosTmpClip[1], infosTmpClip[2], int(infosTmpClip[3])

        positionTmpClip = buttleData.getGraphWrapper().getPositionClip(tmpClipNodeName, tmpClipName, tmpClipNumber)
        tmpClip = IdClip(tmpClipNodeName, tmpClipName, tmpClipNumber, positionTmpClip)

        if tmpClip:
            positionNewClip = buttleData.getGraphWrapper().getPositionClip(clip.getNodeName(), clip.getName(), clipNumber)
            newClip = IdClip(clip.getNodeName(), clip.getName(), clipNumber, positionNewClip)

            if tmpClip.getName() == "Output":
                clipOut = tmpClip
                clipIn = newClip
            else:
                clipOut = newClip
                clipIn = tmpClip

            if buttleData.getGraphWrapper().canConnect(clipOut, clipIn):
                    self.connect(clipOut, clipIn)
                    return

            else:
                connection = buttleData.getGraphWrapper().getConnectionByClips(clipOut, clipIn)
                if connection:
                    self.disconnect(connection)
                    return

        # update undo/redo display
        self.undoRedoChanged()

    def connect(self, clipOut, clipIn):
        """
            Adds a connection between 2 clips.
        """
        buttleData = ButtleDataSingleton().get()
        connection = buttleData.getGraph().createConnection(clipOut, clipIn)
        # link signal changed of the connection to a global signal ViewerChangedSignal
        connection.changed.connect(buttleData.emitViewerChangedSignal)

    def disconnect(self, connection):
        """
            Removes a connection between 2 clips.
        """
        buttleData = ButtleDataSingleton().get()
        buttleData.getGraph().deleteConnection(connection)

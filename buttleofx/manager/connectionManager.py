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

        infosTmpCLip = dataTmpClip.split("/")
        if infosTmpCLip[0] != "clip" or len(infosTmpCLip) != 4:
            return

        positionTmpCLip = buttleData.getGraphWrapper().getPositionClip(infosTmpCLip[1], infosTmpCLip[2], int(infosTmpCLip[3]))
        tmpClip = IdClip(infosTmpCLip[1], infosTmpCLip[2], infosTmpCLip[3], positionTmpCLip)

        if tmpClip:
            positionNewClip = buttleData.getGraphWrapper().getPositionClip(clip.getNodeName(), clip.getName(), clipNumber)
            newClip = IdClip(clip.getNodeName(), clip.getName(), clipNumber, positionNewClip)

            if buttleData.getGraphWrapper().canConnect(tmpClip, newClip):
                self.connect(tmpClip, newClip)
                return

            elif buttleData.getGraph().contains(tmpClip) and buttleData.getGraph().contains(newClip):
                self.disconnect(buttleData.getGraphWrapper().getConnectionByClips(tmpClip, newClip))
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

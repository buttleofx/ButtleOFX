# quickmamba
from quickmamba.patterns import Singleton
# data
from buttleofx.data import ButtleDataSingleton
# connection
from buttleofx.core.graph.connection import IdClip


class ConnectionManager(Singleton):
    """
        This class manages actions about connections.
    """

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

        print "Unable to connect or disconnect the nodes."

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

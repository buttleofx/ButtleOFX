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

        print "Unable to connect or delete the nodes."

    def connect(self, clipOut, clipIn):
        """
            Adds a connection between 2 clips.
        """
        buttleData = ButtleDataSingleton().get()
        buttleData.getGraph().createConnection(clipOut, clipIn)

    def disconnect(self, connection):
        """
            Removes a connection between 2 clips.
        """
        buttleData = ButtleDataSingleton().get()
        buttleData.getGraph().deleteConnection(connection)

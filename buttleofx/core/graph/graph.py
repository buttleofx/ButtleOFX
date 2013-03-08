import logging
# Tuttle
from pyTuttle import tuttle
# quickmamba
from quickmamba.patterns import Signal
#undo_redo
from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.core.undo_redo.commands.node import CmdCreateNode, CmdDeleteNodes, CmdCreateReaderNode, CmdSetCoord
from buttleofx.core.undo_redo.commands.connection import CmdCreateConnection, CmdDeleteConnection


class Graph(object):
    """
        Class Graph contains :
            - _graphTuttle : the tuttle graph

            - _nodes : list of buttle nodes (python objects, the core nodes)
            - _connections : list of buttle connections (python objects, the core connections)

            Signals :
                - nodesChanged : the signal emited when a node changed
                - connectionsChanged : the signal emited when a connection changed
                - connectionsCoordChanged : the signal emited when the coords of a connection changed (it's a trick in QML)
    """

    def __init__(self):
        self._graphTuttle = tuttle.Graph()
        #self._graphTuttle.setup() # good idea ?

        self._nodes = []
        self._connections = []

        # signals
        self.nodesChanged = Signal()
        self.connectionsChanged = Signal()
        self.connectionsCoordChanged = Signal()

        logging.info("Core : Graph created")

    def __str__(self):
        """
            Displays on terminal some data.
            Usefull to debug the class.
        """
        str_list = []

        str_list.append("=== Graph Buttle === \n")
        str_list.append("---- all nodes ---- \n")

        for node in self._nodes:
            str_list.append(node.__str__())
            str_list.append("\n")

        str_list.append("---- all connections ----")
        for con in self._connections:
            str_list.append(con.__str__())
            str_list.append("\n")

        return "".join(str_list)

    ################################################## ACCESSORS ##################################################

    def getNodes(self):
        """
            Returns the node List.
        """
        return self._nodes

    def getNode(self, nodeName):
        for node in self._nodes:
            if node.getName() == nodeName:
                return node
        return None

    def getConnections(self):
        """
            Returns the connection List.
        """
        return self._connections

    def getConnectionByClips(self, clipOut, clipIn):
        for connection in self._connections:
            if connection.getClipOut() == clipOut and connection.getClipIn() == clipIn:
                return connection
        return None

    def getConnectionById(self, connectionId):
        for connection in self._connections:
            if connection.getId() == connectionId:
                return connection
        return None

    def getGraphTuttle(self):
        """
            Return the Tuttle's graph.
        """
        return self._graphTuttle

    ################################################## CREATION & DESTRUCTION ##################################################

    def createNode(self, nodeType, x, y):
        """
            Adds a node from the node list when a node is created.
        """
        cmdCreateNode = CmdCreateNode(self, nodeType, x, y)
        cmdManager = CommandManager()
        return cmdManager.push(cmdCreateNode)

    def createReaderNode(self, url, x, y):
        """
            Creates a reader node when an image has been dropped in the graph.
        """
        extension = url.split(".")[-1].lower()
        print extension

        if extension in ['jpeg', 'jpg', 'jpe', 'jfif', 'jfi']:
            nodeType = 'tuttle.jpegreader'
        elif extension == 'png':
            nodeType = 'tuttle.pngreader'
        elif extension in ['mpeg', 'mp4', 'avi', 'mov', 'aac', 'ac3', 'adf', 'adx', 'aea', 'ape', 'apl', 'mac', 'bin', 'bit', 'bmv', 'cdg', 'cdxl', 'xl', '302', 'daud', 'dts', 'dv', 'dif', 'cdata', 'eac3', 'flm', 'flac', 'flv', 'g722', '722', 'tco', 'rco', 'g723_1', 'g729', 'gsm', 'h261', 'h26l', 'h264', '264', 'idf', 'cgi', 'latm', 'm4v', 'mjpg', 'mjpeg', 'mpo', 'mlp', 'mp2', 'mp3', 'm2a', 'mpc', 'mvi', 'mxg', 'v', 'nut', 'ogg', 'oma', 'omg', 'aa3', 'al', 'ul', 'sw', 'sb', 'uw', 'ub', 'yuv', 'cif', 'qcif', 'rgb', 'rt', 'rso', 'smi', 'sami', 'sbg', 'shn', 'vb', 'son', 'mjpg', 'sub', 'thd', 'tta', 'ans', 'art', 'asc', 'diz', 'ice', 'nfo', 'txt', 'vt', 'vc1', 'vqf', 'vql', 'vqe', 'vtt', 'yop', 'y4m']:
            nodeType = 'tuttle.ffmpegreader'
        elif extension in ['3fr', 'ari', 'arw', 'bay', 'crw', 'cr2', 'cap', 'dng', 'dcs', 'dcr', 'dng', 'drf', 'eip', 'erf', 'fff', 'iiq', 'k25', 'kdc', 'mef', 'mos', 'mrw', 'nef', 'nrw', 'obm', 'orf', 'pef', 'ptx', 'pxn', 'r3d', 'rad', 'raf', 'rw2', 'raw', 'rwl', 'rwz', 'srf', 'sr2', 'srw', 'x3f']:
            nodeType = 'tuttle.rawreader'
        elif extension in ['aai', 'art', 'arw', 'avi', 'avs', 'bmp', 'bmp2', 'bmp3', 'cals', 'cgm', 'cin', 'cmyk', 'cmyka', 'cr2', 'crw', 'cur', 'cut', 'dcm', 'dcr', 'dcx', 'dib', 'djvu', 'dng', 'dot', 'dpx', 'emf', 'epdf', 'epi', 'eps', 'eps2', 'eps3', 'epsf', 'epsi', 'ept', 'exr', 'fax', 'fig', 'fits', 'fpx', 'gif', 'gplt', 'gray', 'hdr', 'hpgl', 'hrz', 'html', 'ico', 'info', 'inline', 'jbig', 'jng', 'jp2', 'jpc', 'jpg', 'jpeg', 'man', 'mat', 'miff', 'mono', 'mng', 'm2v', 'mpeg', 'mpc', 'mpr', 'mrw', 'msl', 'mtv', 'mvg', 'nef', 'orf', 'otb', 'p7', 'palm', 'pam', 'pbm', 'pcd', 'pcds', 'pcl', 'pcx', 'pdb', 'pdf', 'pef', 'pfa', 'pfb', 'pfm', 'pgm', 'picon', 'pict', 'pix', 'png', 'png8', 'png16', 'png32', 'pnm', 'ppm', 'ps', 'ps2', 'ps3', 'psb', 'psd', 'ptif', 'pwp', 'rad', 'rgb', 'rgba', 'rla', 'rle', 'sct', 'sfw', 'sgi', 'shtml', 'sid', 'mrsid', 'sun', 'svg', 'tga', 'tiff', 'tim', 'tif', 'txt', 'uil', 'uyvy', 'vicar', 'viff', 'wbmp', 'webp', 'wmf', 'wpg', 'x', 'xbm', 'xcf', 'xpm', 'xwd', 'x3f', 'ycbcr', 'ycbcra', 'yuv']:
            nodeType = 'tuttle.imagemagickreader'
        elif extension in ['bmp', 'cin', 'dds', 'dpx', 'exr', 'fits', 'hdr', 'ico', 'j2k', 'j2c', 'jp2', 'jpeg', 'jpg', 'jpe', 'jfif', 'jfi', 'pbm', 'pgm', 'png', 'pnm', 'ppm', 'pic', 'psd', 'rgbe', 'sgi', 'tga', 'tif', 'tiff', 'tpic', 'tx', 'webp']:
            nodeType = 'tuttle.oiioreader'
        else:
            print "Unknown format. Can't create reader node."
            return
            #use exception !

        # create the node
        #########################
        # use a group of command : 
        # - create node
        # - setParamString
        #########################
        cmdCreateReaderNode = CmdCreateReaderNode(self, nodeType, x, y, url)
        cmdManager = CommandManager()
        return cmdManager.push(cmdCreateReaderNode)

    def deleteNodes(self, nodes):
        """
            Removes a node in the node list when a node is deleted.
        """
        cmdDeleteNodes = CmdDeleteNodes(self, nodes)
        cmdManager = CommandManager()
        cmdManager.push(cmdDeleteNodes)

    def createConnection(self, clipOut, clipIn):
        """
            Adds a connection in the connection list when a connection is created.
        """
        cmdCreateConnection = CmdCreateConnection(self, clipOut, clipIn)
        cmdManager = CommandManager()
        return cmdManager.push(cmdCreateConnection)

    def deleteConnection(self, connection):
        """
            Removes a connection.
        """
        cmdDeleteConnection = CmdDeleteConnection(self, connection)
        cmdManager = CommandManager()
        cmdManager.push(cmdDeleteConnection)

    def deleteNodeConnections(self, nodeName):
        """
            Removes all the connections of the node.
        """
        # We have to rebuild the list of connections, based on the current values.
        self._connections = [connection for connection in self._connections if not (connection.getClipOut().getNodeName() == nodeName or connection.getClipIn().getNodeName() == nodeName)]

    ############################################### INTERACTION ###############################################

    def nodeMoved(self, nodeName, x, y):
        """
            This fonction push a cmdMoved in the CommandManager.
        """
        # only push a cmd if the node truly moved
        if self.getNode(nodeName).getOldCoord() != (x, y):
            cmdMoved = CmdSetCoord(self, nodeName, (x, y))
            cmdManager = CommandManager()
            cmdManager.push(cmdMoved)

    ################################################## FLAGS ##################################################

    def contains(self, clip):
        """
            Returns True if the clip is already connected, else False.
        """
        for connection in self._connections:
            if (clip == connection.getClipOut() or clip == connection.getClipIn()):
                return True
        return False

    def nodesConnected(self, clipOut, clipIn):
        """
            Returns True if the nodes containing the clips are already connected (in the other direction).
        """
        for connection in self._connections:
            if (clipOut.getNodeName() == connection.getClipIn().getNodeName() and clipIn.getNodeName() == connection.getClipOut().getNodeName()):
                return True
        return False

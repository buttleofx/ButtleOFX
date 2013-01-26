# Tuttle
from pyTuttle import tuttle
#undo_redo
from buttleofx.core.undo_redo.manageTools import CommandManager, GroupUndoableCommands
from buttleofx.core.undo_redo.commands import CmdCreateNode, CmdDeleteNode, CmdCreateConnection, CmdDeleteConnection, CmdCreateReaderNode
# quickmamba
from quickmamba.patterns import Signal


class Graph(object):
    """
        Class Graph contains
        - _nodes : list of nodes (python objects, the core nodes)
        - _connections : list of connections (python objects, the core connections)
        - nodesChanged : the signal emited to the wrapper layer to update nodeWrappers
        - connectionsChanged : the signal emited to the wrapper layer to update connectionWrappers
    """

    def __init__(self):
        self._graphTuttle = tuttle.Graph()

        self._nodes = []
        self._connections = []

        self.nodesChanged = Signal()
        self.connectionsChanged = Signal()
        self.connectionsCoordChanged = Signal()

        print "Core : Graph created"

    def __str__(self):
        """
            Displays on terminal some data.
            Usefull to debug the class.
        """

        print("=== Graph Buttle ===")
        print("---- all nodes ----")
        for node in self._nodes:
            print node

        print("---- all connections ----")
        for con in self._connections:
            print con

        print("=== Graph Tuttle ===")
        print self._graphTuttle

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
        cmdManager.push(cmdCreateNode)

    def createReaderNode(self, url, x, y):
        """
            Creates a reader node when an image has been dropped in the graph.
        """
        extension = url.split(".")[-1].lower()
        print extension

        if extension in ['jpeg', 'jpg', 'jpe', 'jfif', 'jfi']:
            nodeType = 'tuttle.turbojpegreader'
        elif extension == 'png':
            nodeType = 'tuttle.pngreader'
        elif extension in ['avi', 'mov', 'aac', 'ac3', 'adf', 'adx', 'aea', 'ape', 'apl', 'mac', 'bin', 'bit', 'bmv', 'cdg', 'cdxl', 'xl', '302', 'daud', 'dts', 'dv', 'dif', 'cdata', 'eac3', 'flm', 'flac', 'flv', 'g722', '722', 'tco', 'rco', 'g723_1', 'g729', 'gsm', 'h261', 'h26l', 'h264', '264', 'idf', 'cgi', 'latm', 'm4v', 'mjpg', 'mjpeg', 'mpo', 'mlp', 'mp2', 'mp3', 'm2a', 'mpc', 'mvi', 'mxg', 'v', 'nut', 'ogg', 'oma', 'omg', 'aa3', 'al', 'ul', 'sw', 'sb', 'uw', 'ub', 'yuv', 'cif', 'qcif', 'rgb', 'rt', 'rso', 'smi', 'sami', 'sbg', 'shn', 'vb', 'son', 'mjpg', 'sub', 'thd', 'tta', 'ans', 'art', 'asc', 'diz', 'ice', 'nfo', 'txt', 'vt', 'vc1', 'vqf', 'vql', 'vqe', 'vtt', 'yop', 'y4m']:
            nodeType = 'tuttle.ffmpegreader'
        elif extension in ['bmp', 'cin', 'dds', 'dpx', 'exr', 'fits', 'hdr', 'ico', 'j2k', 'j2c', 'jp2', 'jpeg', 'jpg', 'jpe', 'jfif', 'jfi', 'pbm', 'pgm', 'png', 'pnm', 'ppm', 'pic', 'psd', 'rgbe', 'sgi', 'tga', 'tif', 'tiff', 'tpic', 'tx', 'webp']:
            nodeType = 'tuttle.oiioreader'
        elif extension in ['3fr', 'ari', 'arw', 'bay', 'crw', 'cr2', 'cap', 'dng', 'dcs', 'dcr', 'dng', 'drf', 'eip', 'erf', 'fff', 'iiq', 'k25', 'kdc', 'mef', 'mos', 'mrw', 'nef', 'nrw', 'obm', 'orf', 'pef', 'ptx', 'pxn', 'r3d', 'rad', 'raf', 'rw2', 'raw', 'rwl', 'rwz', 'srf', 'sr2', 'srw', 'x3f']:
            nodeType = 'tuttle.rawreader'
        elif extension in ['aai', 'art', 'arw', 'avi', 'avs', 'bmp', 'bmp2', 'bmp3', 'cals', 'cgm', 'cin', 'cmyk', 'cmyka', 'cr2', 'crw', 'cur', 'cut', 'dcm', 'dcr', 'dcx', 'dib', 'djvu', 'dng', 'dot', 'dpx', 'emf', 'epdf', 'epi', 'eps', 'eps2', 'eps3', 'epsf', 'epsi', 'ept', 'exr', 'fax', 'fig', 'fits', 'fpx', 'gif', 'gplt', 'gray', 'hdr', 'hpgl', 'hrz', 'html', 'ico', 'info', 'inline', 'jbig', 'jng', 'jp2', 'jpc', 'jpg', 'jpeg', 'man', 'mat', 'miff', 'mono', 'mng', 'm2v', 'mpeg', 'mpc', 'mpr', 'mrw', 'msl', 'mtv', 'mvg', 'nef', 'orf', 'otb', 'p7', 'palm', 'pam', 'pbm', 'pcd', 'pcds', 'pcl', 'pcx', 'pdb', 'pdf', 'pef', 'pfa', 'pfb', 'pfm', 'pgm', 'picon', 'pict', 'pix', 'png', 'png8', 'png16', 'png32', 'pnm', 'ppm', 'ps', 'ps2', 'ps3', 'psb', 'psd', 'ptif', 'pwp', 'rad', 'rgb', 'rgba', 'rla', 'rle', 'sct', 'sfw', 'sgi', 'shtml', 'sid', 'mrsid', 'sun', 'svg', 'tga', 'tiff', 'tim', 'tif', 'txt', 'uil', 'uyvy', 'vicar', 'viff', 'wbmp', 'webp', 'wmf', 'wpg', 'x', 'xbm', 'xcf', 'xpm', 'xwd', 'x3f', 'ycbcr', 'ycbcra', 'yuv']:
            nodeType = 'tuttle.imagemagickreader'
        else:
            print "Unknown format. Can't create reader node."
            return
            #use exception !

        # create the node
        cmdCreateReaderNode = CmdCreateReaderNode(self, nodeType, x, y, url)
        cmdManager = CommandManager()
        cmdManager.push(cmdCreateReaderNode)

    def deleteNode(self, node):
        """
            Removes a node in the node list when a node is deleted.
        """
        cmdDeleteNode = CmdDeleteNode(self, node)
        cmdManager = CommandManager()
        cmdManager.push(cmdDeleteNode)

    def createConnection(self, clipOut, clipIn):
        """
            Adds a connection in the connection list when a connection is created.
        """
        cmdCreateConnection = CmdCreateConnection(self, clipOut, clipIn)
        cmdManager = CommandManager()
        cmdManager.push(cmdCreateConnection)

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
        # We can't use a for loop. We have to rebuild the list, based on the current values.
        self._connections = [connection for connection in self._connections if not (connection.getClipOut().getNodeName() == nodeName or connection.getClipIn().getNodeName() == nodeName)]
        self.connectionsChanged()

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

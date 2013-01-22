from pyTuttle import tuttle
from PySide.QtCore import *
from PySide.QtGui import *
from pluginViewer import Ui_TuttlePlugins
import sys


def setUp():
    tuttle.core().preload()

def getPlugins():
    pluginCache = tuttle.core().getPluginCache()
    return pluginCache.getPlugins()

def getPluginsNames():
    pluginCache = tuttle.core().getPluginCache()
    return [p.getIdentifier() for p in pluginCache.getPlugins()]

def getPlugin( name ):
    listOfPlugins = []
    plugins = getPlugins()
    for plugin in plugins :
        if( name == plugin.getIdentifier() ):
            listOfPlugins.append(plugin);
    return listOfPlugins

class OfxInt2D(QFrame):
        d1 = None
        d2 = None

        def __init__( self, parent = None ):
                super( OfxInt2D, self ).__init__( parent )
                grid = QGridLayout( self )

                self.d1 = QSpinBox( )
                self.d2 = QSpinBox( )
                grid.addWidget( self.d1, 0, 0 )
                grid.addWidget( self.d2, 0, 1 )

class OfxDouble2D(QFrame):
        d1 = None
        d2 = None

        def __init__( self, parent = None ):
                super( OfxDouble2D, self ).__init__( parent )
                grid = QGridLayout( self )

                self.d1 = QDoubleSpinBox( )
                self.d2 = QDoubleSpinBox( )
                grid.addWidget( self.d1, 0, 0 )
                grid.addWidget( self.d2, 0, 1 )

class OfxInt3D(QFrame):
        d1 = None
        d2 = None
        d3 = None

        def __init__( self, parent = None ):
                super( OfxInt3D, self ).__init__( parent )
                grid = QGridLayout( self )

                self.d1 = QSpinBox( )
                self.d2 = QSpinBox( )
                self.d3 = QSpinBox( )
                grid.addWidget( self.d1, 0, 0 )
                grid.addWidget( self.d2, 0, 1 )
                grid.addWidget( self.d3, 0, 1 )

class OfxDouble3D(QFrame):
        d1 = None
        d2 = None
        d3 = None

        def __init__( self, parent = None ):
                super( OfxDouble3D, self ).__init__( parent )
                grid = QGridLayout( self )

                self.d1 = QDoubleSpinBox( )
                self.d2 = QDoubleSpinBox( )
                self.d3 = QDoubleSpinBox( )
                grid.addWidget( self.d1, 0, 0 )
                grid.addWidget( self.d2, 0, 1 )
                grid.addWidget( self.d3, 0, 1 )

class OfxRGB(QFrame):
        sr = None
        sg = None
        sb = None

        def __init__( self, parent = None ):
                super( OfxRGB, self ).__init__( parent )
                grid = QGridLayout( self )

                self.sr = QDoubleSpinBox( )
                self.sg = QDoubleSpinBox( )
                self.sb = QDoubleSpinBox( )
                b  = QPushButton( "pick" )
                self.sr.setStyleSheet("QDoubleSpinBox { background-color: #863838 }")
                self.sg.setStyleSheet("QDoubleSpinBox { background-color: #437037 }")
                self.sb.setStyleSheet("QDoubleSpinBox { background-color: #344770 }")
                grid.addWidget( self.sr, 0, 0 )
                grid.addWidget( self.sg, 0, 1 )
                grid.addWidget( self.sb, 0, 2 )
                grid.addWidget( b , 0, 4 )

                b.pressed.connect( self.openColorDialog )

        def openColorDialog( self ):
                col = QColorDialog.getColor()
                self.sr.setValue( col.red() )
                self.sg.setValue( col.green() )
                self.sb.setValue( col.blue() )

class OfxRGBA(QFrame):
    sr = None
    sg = None
    sb = None
    sa = None

    def __init__( self, parent = None ):
        super( OfxRGBA, self ).__init__( parent )
                grid = QGridLayout( self )

                self.sr = QDoubleSpinBox( )
                self.sg = QDoubleSpinBox( )
                self.sb = QDoubleSpinBox( )
                self.sa = QDoubleSpinBox( )
                b  = QPushButton( "pick" )
                self.sr.setStyleSheet("QDoubleSpinBox { background-color: #863838 }")
                self.sg.setStyleSheet("QDoubleSpinBox { background-color: #437037 }")
                self.sb.setStyleSheet("QDoubleSpinBox { background-color: #344770 }")
        grid.addWidget( self.sr, 0, 0 )
        grid.addWidget( self.sg, 0, 1 )
        grid.addWidget( self.sb, 0, 2 )
        grid.addWidget( self.sa, 0, 3 )
        grid.addWidget( b , 0, 4 )

        b.pressed.connect( self.openColorDialog )

    def openColorDialog( self ):
                col = QColorDialog.getColor()
        self.sr.setValue( col.red() )
        self.sg.setValue( col.green() )
        self.sb.setValue( col.blue() )

class TuttleMainWindow(QMainWindow):
    def __init__( self, parent = None ):
        super( TuttleMainWindow, self ).__init__( parent )
        self.createWidgets()

    def createWidgets( self ):
        self.ui = Ui_TuttlePlugins()
        self.ui.setupUi( self )

        def connect( self ):
                self.ui.treeWidget.itemActivated.connect(self.selected)

    def updatePluginList( self ):
        plugins = getPluginsNames()
                items = QTreeWidgetItem( 0 )
                items.setText( 0, "plugins" )

        for plugin in plugins:
                        g = tuttle.Graph()
                        p = g.createNode( plugin )
                        node = p.asImageEffectNode()

                        grouping = node.getProperties().fetchProperty("OfxImageEffectPluginPropGrouping").getStringValue(0)
                        grouping = grouping.split('/')

                        groupingList = []
                        for gr in grouping :
                            groupingList = groupingList + gr.split()

                        item = None
                        found = False
                        for i in range( items.childCount() ) :
                            if items.child( i ).text(0) == groupingList[0] :
                                item = items.child( i )
                                found = True

                        if not found:
                                item = QTreeWidgetItem( items )
                                item.setText( 0, groupingList[0] )
                                #iconPath = getPlugin( plugin )[0].getBinary().getBundlePath() + '/Contents/Resources/' + groupingList[0] + '.svg'
                                iconPath = getPlugin( plugin )[0].getBinary().getBundlePath() + '/Contents/Resources/' + groupingList[0] + '.png'
                                item.setIcon( 0, QIcon( iconPath ) )

                        parent = item

                        pluginRoot = groupingList[0]

                        for label in groupingList[1:] :
                            child = None
                            foundChild = False
                            pluginRoot = pluginRoot + '/' + label
                            for i in range( parent.childCount() ) :
                                if parent.child( i ).text(0) == label :
                                    child = parent.child( i )
                                    foundChild = True

                            if not foundChild:
                                child = QTreeWidgetItem( 0 )
                                child.setText( 0, label )
                                #iconPath = getPlugin( plugin )[0].getBinary().getBundlePath() + '/Contents/Resources/' + pluginRoot + '.svg'
                                iconPath = getPlugin( plugin )[0].getBinary().getBundlePath() + '/Contents/Resources/' + pluginRoot + '.png'
                                child.setIcon( 0, QIcon( iconPath ) )
                                parent.addChild( child )
                            parent = child

                        # add plugin
                        child = QTreeWidgetItem( 0 )
                        pluginLabel = node.getProperties().fetchProperty("OfxPropLabel").getStringValue(0)
                        child.setText( 0, pluginLabel )
                        child.setText( 1, getPlugin( plugin )[0].getIdentifier() )
                        parent.addChild( child )

                        rawIdentifier = getPlugin( plugin )[0].getRawIdentifier()

                        #iconPath = getPlugin( plugin )[0].getBinary().getBundlePath() + '/Contents/Resources/' + rawIdentifier + '.svg'
                        iconPath = getPlugin( plugin )[0].getBinary().getBundlePath() + '/Contents/Resources/' + rawIdentifier + '.png'
                        child.setIcon( 0, QIcon( iconPath ) )

                self.ui.treeWidget.addTopLevelItem ( items )

        def selected( self, item ):
                if item.columnCount() == 1:
                    return
                plugins = getPlugin( item.text(1) )
        plugin = plugins[0]

        self.ui.pluginName.setText( plugin.getIdentifier() )
        self.ui.pluginRawName.setText( plugin.getRawIdentifier() )
        self.ui.pluginVersion.clear()
        for plugin in plugins :
            self.ui.pluginVersion.addItem( str(plugin.getVersionMajor()) + "." + str(plugin.getVersionMinor()) )

        g = tuttle.Graph()
        p = g.createNode( plugin.getIdentifier() )
        node = p.asImageEffectNode()

        for i in range( self.ui.gridParameters.count() ):
            self.ui.gridParameters.itemAt(i).widget().close()

                pageList = []
                pageListName = []
                groupList = []
                groupListName = []

        line = 0
        column = 0
        for pIdx in range( node.getNbParams() ) :
            param = node.getParam( pIdx )
                        #print param
                        nodeLabel = QLabel( param.getProperties().fetchProperty("OfxPropName").getStringValue(0) )

            nodeType = param.getProperties().fetchProperty("OfxParamPropType").getStringValue(0)
            paramEditor = None
            if nodeType == "OfxParamTypeInteger" :
                                paramEditor = QSpinBox( )
                value = param.getProperties().fetchProperty("OfxParamPropDefault").getStringValue( 0 )
                paramEditor.setValue( int( value ) )
            if nodeType == "OfxParamTypeDouble" :
                                paramEditor = QDoubleSpinBox( )
                value = param.getProperties().fetchProperty("OfxParamPropDefault").getStringValue( 0 )
                                #paramEditor.setValue( float( value ) )
            if nodeType == "OfxParamTypeBoolean" :
                                paramEditor = QCheckBox( )
                value = param.getProperties().fetchProperty("OfxParamPropDefault").getStringValue( 0 )
                state = None
                if value == 1 :
                                        state = Qt.Checked
                else:
                                        state = Qt.Unchecked
                paramEditor.setCheckState( state )
            if nodeType == "OfxParamTypeChoice" :
                                paramEditor = QComboBox( )
                for choiceOpt in range( param.getProperties().fetchProperty("OfxParamPropChoiceOption").getDimension() ):
                    paramEditor.insertItem( 0,  param.getProperties().fetchProperty("OfxParamPropChoiceOption").getStringValue( choiceOpt ) )
            if nodeType == "OfxParamTypeRGBA" :
                paramEditor = OfxRGBA()

            if nodeType == "OfxParamTypeRGB" :
                                paramEditor = OfxRGBA()

            if nodeType == "OfxParamTypeDouble2D" :
                                paramEditor = OfxDouble2D()

            if nodeType == "OfxParamTypeInteger2D" :
                                paramEditor = OfxInt2D()

            if nodeType == "OfxParamTypeDouble3D" :
                                paramEditor = OfxDouble3D()

            if nodeType == "OfxParamTypeInteger3D" :
                                paramEditor = OfxInt3D()

            if nodeType == "OfxParamTypeString" :
                stringMode = param.getProperties().fetchProperty("OfxParamPropStringMode").getStringValue(0)
                if stringMode == "OfxParamStringIsSingleLine" :
                                        paramEditor = QLineEdit()
                if stringMode == "OfxParamStringIsMultiLine" :
                                        paramEditor = QTextEdit()
                if stringMode == "OfxParamStringIsFilePath" :
                                        paramEditor = QWidget()
                                        grid = QGridLayout( paramEditor )
                                        filename = QLineEdit( )
                                        button = QPushButton( "browse file" )
                    grid.addWidget( filename, 0, 0 )
                    grid.addWidget( button, 0, 1 )
                if stringMode == "OfxParamStringIsDirectoryPath" :
                                        paramEditor = QWidget()
                                        grid = QGridLayout( paramEditor )
                                        directory = QLineEdit( )
                                        button = QPushButton( "browse directory" )
                    grid.addWidget( directory, 0, 0 )
                    grid.addWidget( button, 0, 1 )
                if stringMode == "OfxParamStringIsLabel" :
                                        paramEditor = QLineEdit()


            if nodeType == "OfxParamTypeCustom" :
                                paramEditor = QLabel( "custom ...")
                        if nodeType == "OfxParamTypeGroup" :
                                paramEditor = QGroupBox( param.getProperties().fetchProperty("OfxPropLabel").getStringValue(0) )
                                subGrid = QGridLayout();
                                paramEditor.setLayout( subGrid );
                                groupList.append( subGrid )
                                groupListName.append( param.getProperties().fetchProperty("OfxPropName").getStringValue(0) )
                                nodeLabel = ""
            if nodeType == "OfxParamTypePage" :
                                paramEditor = QLabel( "page : " + param.getProperties().fetchProperty("OfxPropLabel").getStringValue(0) )
                                nodeLabel = ""
            if nodeType == "OfxParamTypePushButton" :
                                paramEditor = QPushButton( param.getProperties().fetchProperty("OfxPropLabel").getStringValue(0)  )
                                nodeLabel = ""


                        parentWidget = self.ui.gridParameters

                        parent = param.getProperties().fetchProperty("OfxParamPropParent").getStringValue(0)

                        if parent != "":
                            index = 0
                            for group in groupListName:
                                index = index + 1
                                if group.title().lower() == parent.lower():
                                    parentWidget = groupList[ index - 1 ]

                        if nodeLabel == "":
                            parentWidget.addWidget( paramEditor, line, column, 1, 2 )
                        else:
                            parentWidget.addWidget( nodeLabel, line, column )
                            parentWidget.addWidget( paramEditor, line, column+1 )

                        line += 1

if __name__ == "__main__":
        setUp()
        app = QApplication( sys.argv )
    browse = TuttleMainWindow(None)
    browse.updatePluginList()
    browse.connect()
    browse.show()
    app.exec_()

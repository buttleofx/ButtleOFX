import QtQuick 2.0
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0
import QtQml 2.1
import QuickMamba 1.0
import QtQuick.Dialogs 1.1
import QtQuick.Window 2.1
import QtQuick.LocalStorage 2.0

import "gui/graph/qml"
import "gui/viewer/qml"
import "gui/paramEditor/qml"
import "gui/browser/qml"
import "gui/plugin/qml"
import "gui/shortcut/qml"

ApplicationWindow {

    property var db: null

    function openDB() {
        if(db == null){
            db = LocalStorage.openDatabaseSync("configFile", "2.0","configViewFile", 100000);
        }
    }


    function saveSetting(key, value) {
        openDB();
        db.transaction( function(tx){
            tx.executeSql('INSERT OR REPLACE INTO settings VALUES(?, ?)', [key, value]);
        });
    }

    function getSetting(key) {
        openDB();
        var res = "";
        db.transaction(function(tx) {
            res = tx.executeSql('SELECT value FROM settings WHERE key=?;', [key]).rows.item(0).value;
        });
        return res;
    }

    property int selectedView: getSetting("view") ? getSetting("view") : 3

    property variant lastSelectedDefaultView: view1
    property variant view1: [browser, paramEditor, player, graphEditor]
    property variant view2: [player, paramEditor, browser, graphEditor]
    property variant view3: [player, browser, advancedParamEditor, graphEditor]

    property string urlOfFileToSave: ""

    width: 1200
    height: 800
    id: mainWindowQML
    title:"ButtleOFX"

    //TopFocusHandler {
    // //anchors.fill: parent
    //}

    Keys.onPressed: {

        // Viewer
        if ((event.key == Qt.Key_1) && (event.modifiers & Qt.KeypadModifier)){
            player.changeViewer(1)
        }
        if ((event.key == Qt.Key_2) && (event.modifiers & Qt.KeypadModifier)){

            player.changeViewer(2)
        }
        if ((event.key == Qt.Key_3) && (event.modifiers & Qt.KeypadModifier)){
            player.changeViewer(3)
        }
        if ((event.key == Qt.Key_4) && (event.modifiers & Qt.KeypadModifier)){
            player.changeViewer(4)
        }
        if ((event.key == Qt.Key_5) && (event.modifiers & Qt.KeypadModifier)){
            player.changeViewer(5)
        }
        if ((event.key == Qt.Key_6) && (event.modifiers & Qt.KeypadModifier)){
            player.changeViewer(6)
        }
        if ((event.key == Qt.Key_7) && (event.modifiers & Qt.KeypadModifier)){
            player.changeViewer(7)
        }
        if ((event.key == Qt.Key_8) && (event.modifiers & Qt.KeypadModifier)){
            player.changeViewer(8)
        }
        if ((event.key == Qt.Key_9) && (event.modifiers & Qt.KeypadModifier)){
            player.changeViewer(9)
        }

        // Player
        if (event.key == Qt.Key_Space && player.node != null) {
            if(player.isPlaying) {
                player.doAction("pause");
            }
            else {
                player.doAction("play");
            }
        }
    }

    property bool aNodeIsSelected:true

    //Window of hint for plugins
    PluginWindow {
        id: doc
        title: "Plugin's Documentation"
        selectedNodeType:_buttleData.currentSelectedNodeWrappers.count!=0? _buttleData.currentSelectedNodeWrappers.get(0).nodeType:""
        selectedNodeDoc:_buttleData.currentSelectedNodeWrappers.count!=0? _buttleData.currentSelectedNodeWrappers.get(0).pluginDoc:""
        selectedNodeGroup:_buttleData.currentSelectedNodeWrappers.count!=0? _buttleData.currentSelectedNodeWrappers.get(0).pluginGroup:""
    }

    //Window of shortcuts
    ShortcutWindow {
        id: shortcuts
        title: "Shortcuts"
    }

    FinderLoadGraph{ id: finderLoadGraph; onGetFileUrl: urlOfFileToSave = fileurl }
    FinderSaveGraph{ id: finderSaveGraph; onGetFileUrl: urlOfFileToSave = fileurl }

    MessageDialog {
        id: openGraph
        title:urlOfFileToSave==""? "Save the new graph?":"Save " + _buttleData.getFileName(urlOfFileToSave) + "?"
        icon: StandardIcon.Warning
        text: "You do not have save the current graph, do you want to save it?"
        detailedText: "If you don't save the graph, last modifications not saved will be lost. "
        standardButtons: StandardButton.Yes | StandardButton.No | StandardButton.Abort
        Component.onCompleted: visible = false
        onYes: {
            if(urlOfFileToSave!=""){
                _buttleData.saveData(urlOfFileToSave)
            }
            else{
                finderSaveGraph.open()
            }
        }
        onNo: {
            finderLoadGraph.open()
        }
        onRejected: {}
    }

    MessageDialog {
        id: newGraph
        title: urlOfFileToSave==""? "Save the new graph?":"Save " + _buttleData.getFileName(urlOfFileToSave) + "?"
        icon: StandardIcon.Warning
        text: "You do not have save the current graph, do you want to save it?"
        detailedText: "If you don't save the graph, last modifications not saved will be lost. "
        standardButtons: StandardButton.Yes | StandardButton.No | StandardButton.Abort
        Component.onCompleted: visible = false
        onYes: {
            if(urlOfFileToSave!=""){
                _buttleData.saveData(urlOfFileToSave)
                _buttleData.graphWrapper.deleteGraphWrapper()
                urlOfFileToSave=""
                _buttleManager.clean()
            }
            else{
                finderSaveGraph.open()
                _buttleData.graphWrapper.deleteGraphWrapper()
                urlOfFileToSave=""
                _buttleManager.clean()
            }
        }
        onNo: {
            _buttleData.graphWrapper.deleteGraphWrapper()
            urlOfFileToSave=""
            _buttleManager.clean()
        }
        onRejected: {}
    }

    menuBar: MenuBar {
        Menu {
            title: "File"

            MenuItem {
                text: "Open"
                shortcut: "Ctrl+O"
                onTriggered: {
                    if(!_buttleData.graphCanBeSaved){
                        finderLoadGraph.open()
                    }
                    else{
                        openGraph.open()
                        openGraph.close()
                        openGraph.open()
                    }
                }
            }

            MenuItem {
                text: "Save"
                shortcut: "Ctrl+S"
                enabled: _buttleData.graphCanBeSaved && urlOfFileToSave!="" ? true : false
                onTriggered: _buttleData.saveData(urlOfFileToSave)
            }

            MenuItem {
                text: "Save As"
                shortcut: "Ctrl+Shift+S"
                enabled: _buttleData.graphCanBeSaved ? true : false
                onTriggered: finderSaveGraph.open()
            }

            MenuSeparator { }

            MenuItem {
                id: quitButton
                text: "Exit"
                onTriggered: Qt.quit()
            }
        }

        Menu {
            title: "Edit"

            Menu {
                id: undoRedoStack
                title: "Undo/Redo stack"

                property variant undoRedoList:_buttleData.graphCanBeSaved ? _buttleManager.undoRedoStack:_buttleManager.undoRedoStack

                Instantiator {
                    model: undoRedoStack.undoRedoList
                    MenuItem {
                        text: object
                        onTriggered: {
                            var indexOfElement=_buttleManager.getIndexOfUndoRedoStack(object)
                            var indexInStack=_buttleManager.getIndex()
                            if (indexOfElement < indexInStack) {
                                if(_buttleManager.canUndo) {
                                    _buttleManager.undoNTimes(indexInStack-indexOfElement)
                                }
                            }
                            else{
                                if(_buttleManager.canRedo) {
                                    _buttleManager.redoNTimes(indexOfElement-indexInStack)
                                }
                            }
                        }
                    }
                    onObjectAdded: undoRedoStack.insertItem(index, object)
                    onObjectRemoved: undoRedoStack.removeItem(object)
                }
            }

            MenuItem {
                text: "Undo"
                shortcut: "Ctrl+Z"
                onTriggered:
                    if(_buttleManager.canUndo) {
                        _buttleManager.undo();
                    }
            }

            MenuItem {
                text: "Redo"
                shortcut: "Ctrl+Y"
                onTriggered:
                    if(_buttleManager.canRedo) {
                        _buttleManager.redo();
                    }
            }

            MenuSeparator { }

            MenuItem {
                text: "Copy"
                shortcut: "Ctrl+C"
                onTriggered:
                    if(!_buttleData.currentSelectedNodeWrappers.isEmpty()) {
                        _buttleManager.nodeManager.copyNode()
                        _buttleManager.connectionManager.copyConnections()
                    }
            }

            MenuItem {
                text: "Paste"
                shortcut: "Ctrl+V"
                onTriggered:
                    if(_buttleData.canPaste) {
                        _buttleManager.nodeManager.pasteNode();
                        _buttleManager.connectionManager.pasteConnection()
                    }
            }

            MenuItem {
                text: "Cut"
                shortcut: "Ctrl+X"
                onTriggered:
                    if (!_buttleData.currentSelectedNodeWrappers.isEmpty()) {
                        _buttleManager.nodeManager.cutNode()
                    }
            }

            MenuItem {
                text: "Duplicate"
                shortcut: "Ctrl+D"
                onTriggered:
                    if (!_buttleData.currentSelectedNodeWrappers.isEmpty()) {
                        _buttleManager.nodeManager.duplicationNode()
                    }
            }

            MenuItem {
                text: "Select all"
                shortcut: "Ctrl+A"
                onTriggered: _buttleManager.selectAllNodes()
            }

            MenuItem {
                text: "Delete"
                //shortcut: "del"
                onTriggered: _buttleManager.deleteSelection()
            }
        }

        Menu {
            id: nodesMenu
            title: "Nodes"

            Instantiator {
                model: _buttleData.getMenu(1,"")
                Menu {
                    id: firstMenu
                    title:object
                    __parentContentItem: nodesMenu.__contentItem  // to remove warning

                    Instantiator {
                        model: _buttleData.getPluginsByPath(firstMenu.title)
                        MenuItem {
                            text: object.pluginType
                            onTriggered: {
                                _buttleData.currentGraphIsGraph()
                                _buttleData.currentGraphWrapper = _buttleData.graphWrapper

                                // if before the viewer was showing an image from the brower, we change the currentView
                                if (_buttleData.currentViewerIndex > 9){
                                    _buttleData.currentViewerIndex = player.lastView
                                    if (player.lastNodeWrapper != undefined)
                                        _buttleData.currentViewerNodeWrapper = player.lastNodeWrapper
                                    player.changeViewer(player.lastView)
                                }

                                _buttleManager.nodeManager.creationNode("_buttleData.graph", object.pluginType, 0, 0)
                            }
                        }
                        onObjectAdded: firstMenu.insertItem(index, object)
                        onObjectRemoved: firstMenu.removeItem(object)
                    }

                    Instantiator {
                        model: _buttleData.getMenu(2,firstMenu.title)
                        Menu {
                            id: secondMenu
                            title:object
                            __parentContentItem: nodesMenu.__contentItem  // to remove warning

                            Instantiator {
                                model: _buttleData.getPluginsByPath(secondMenu.title)
                                MenuItem {
                                    text: object.pluginType
                                    onTriggered: {
                                        _buttleData.currentGraphIsGraph()
                                        _buttleData.currentGraphWrapper = _buttleData.graphWrapper

                                        // if before the viewer was showing an image from the brower, we change the currentView
                                        if (_buttleData.currentViewerIndex > 9){
                                            _buttleData.currentViewerIndex = player.lastView
                                            if (player.lastNodeWrapper != undefined)
                                                _buttleData.currentViewerNodeWrapper = player.lastNodeWrapper
                                            player.changeViewer(player.lastView)
                                        }

                                        _buttleManager.nodeManager.creationNode("_buttleData.graph", object.pluginType, 0, 0)
                                    }
                                }
                                onObjectAdded: secondMenu.insertItem(index, object)
                                onObjectRemoved: secondMenu.removeItem(object)
                            }

                            Instantiator {
                                model: _buttleData.getMenu(3,secondMenu.title)
                                Menu {
                                    id: thirdMenu
                                    title:object
                                    __parentContentItem: nodesMenu.__contentItem  // to remove warning

                                    Instantiator {
                                        model: _buttleData.getPluginsByPath(thirdMenu.title)
                                        MenuItem {
                                            text: object.pluginType
                                            onTriggered: {
                                                _buttleData.currentGraphIsGraph()
                                                _buttleData.currentGraphWrapper = _buttleData.graphWrapper

                                                // if before the viewer was showing an image from the brower, we change the currentView
                                                if (_buttleData.currentViewerIndex > 9){
                                                    _buttleData.currentViewerIndex = player.lastView
                                                    if (player.lastNodeWrapper != undefined)
                                                        _buttleData.currentViewerNodeWrapper = player.lastNodeWrapper
                                                    player.changeViewer(player.lastView)
                                                }

                                                _buttleManager.nodeManager.creationNode("_buttleData.graph", object.pluginType, 0, 0)
                                            }
                                        }
                                        onObjectAdded: thirdMenu.insertItem(index, object)
                                        onObjectRemoved: thirdMenu.removeItem(object)
                                    }

                                    Instantiator {
                                        model: _buttleData.getMenu(4,thirdMenu.title)
                                        Menu {
                                            id:fourthMenu
                                            title: object
                                            __parentContentItem: nodesMenu.__contentItem  // to remove warning

                                            Instantiator {
                                                model: _buttleData.getPluginsByPath(fourthMenu.title)
                                                MenuItem {
                                                    text: object.pluginType
                                                    onTriggered: {
                                                        _buttleData.currentGraphIsGraph()
                                                        _buttleData.currentGraphWrapper = _buttleData.graphWrapper

                                                        // if before the viewer was showing an image from the brower, we change the currentView
                                                        if (_buttleData.currentViewerIndex > 9){
                                                            _buttleData.currentViewerIndex = player.lastView
                                                            if (player.lastNodeWrapper != undefined)
                                                                _buttleData.currentViewerNodeWrapper = player.lastNodeWrapper
                                                            player.changeViewer(player.lastView)
                                                        }

                                                        _buttleManager.nodeManager.creationNode("_buttleData.graph", object.pluginType, 0, 0)
                                                    }
                                                }
                                                onObjectAdded: fourthMenu.insertItem(index, object)
                                                onObjectRemoved: fourthMenu.removeItem(object)
                                            }

                                            Instantiator {
                                                model: _buttleData.getMenu(5,fourthMenu.title)
                                                Menu {
                                                    id: fifthMenu
                                                    title: object
                                                    __parentContentItem: nodesMenu.__contentItem  // to remove warning

                                                    Instantiator {
                                                        model: _buttleData.getPluginsByPath(fifthMenu.title)
                                                        MenuItem {
                                                            text: object.pluginType
                                                            onTriggered: {
                                                                _buttleData.currentGraphIsGraph()
                                                                _buttleData.currentGraphWrapper = _buttleData.graphWrapper

                                                                // if before the viewer was showing an image from the brower, we change the currentView
                                                                if (_buttleData.currentViewerIndex > 9){
                                                                    _buttleData.currentViewerIndex = player.lastView
                                                                    if (player.lastNodeWrapper != undefined)
                                                                        _buttleData.currentViewerNodeWrapper = player.lastNodeWrapper
                                                                    player.changeViewer(player.lastView)
                                                                }

                                                                _buttleManager.nodeManager.creationNode("_buttleData.graph", object.pluginType, 0, 0)
                                                            }
                                                        }
                                                        onObjectAdded: fifthMenu.insertItem(index, object)
                                                        onObjectRemoved: fifthMenu.removeItem(object)
                                                    }
                                                }
                                                onObjectAdded: fourthMenu.insertItem(index, object)
                                                onObjectRemoved: fourthMenu.removeItem(object)
                                            }
                                        }
                                        onObjectAdded: thirdMenu.insertItem(index, object)
                                        onObjectRemoved: thirdMenu.removeItem(object)
                                    }
                                }
                                onObjectAdded: secondMenu.insertItem(index, object)
                                onObjectRemoved: secondMenu.removeItem(object)
                            }
                        }
                        onObjectAdded: firstMenu.insertItem(index, object)
                        onObjectRemoved: firstMenu.removeItem(object)
                    }
                }
                onObjectAdded: nodesMenu.insertItem(index, object)
                onObjectRemoved: nodesMenu.removeItem(object)
            }
        }

        Menu {
            id: help
            title: "Help"

            MenuItem {
                text: "Shortcut"
                onTriggered: shortcuts.show()
            }
            MenuItem {
                text: "Plugin's Documentation"
                onTriggered: doc.show()
            }
        }


        Menu {
            title: "View"

            MenuItem {
                id: defaultView
                text: "Default"
                checkable: true
                checked: selectedView==1? true : false
                onTriggered: {
                    checked = true
                    browserView.checked = false
                    advancedView.checked = false
                    selectedView = 1
                    saveSetting("view",selectedView)
                    lastSelectedDefaultView = view1
                    topLeftView.visible=true; bottomLeftView.visible=true; topRightView.visible=true; bottomRightView.visible=true
                    rightColumn.width = 0.7*mainWindowQML.width
                }
            }

            MenuItem {
                id: browserView
                text: "Browser Mode"
                checkable: true
                checked: selectedView==2? true : false
                onTriggered: {
                    checked = true
                    defaultView.checked = false
                    advancedView.checked = false
                    selectedView = 2
                    saveSetting("view",selectedView)
                    lastSelectedDefaultView = view2
                    topLeftView.visible=true; bottomLeftView.visible=true; topRightView.visible=true; bottomRightView.visible=true
                    rightColumn.width = 0.7*mainWindowQML.width
                }
            }

            MenuItem {
                id: advancedView
                text: "Quick Mode"
                checkable: true
                checked: selectedView==3? true : false
                onTriggered: {
                    checked = true
                    defaultView.checked = false
                    browserView.checked = false
                    selectedView = 3
                    saveSetting("view",selectedView)
                    lastSelectedDefaultView = view3
                    topLeftView.visible=true; bottomLeftView.visible=true; topRightView.visible=true; bottomRightView.visible=false
                    rightColumn.width = 0.3*mainWindowQML.width
                }
            }

/*            MenuSeparator { }

            MenuItem {
                text: "Browser"
                checkable: true
                checked: browser.parent.visible==true ? true : false
                onTriggered: browser.parent.visible == false ? browser.parent.visible=true : browser.parent.visible=false
            }

            MenuItem {
                text: "Viewer"
                checkable: true
                checked: player.parent.visible==true ? true : false
                onTriggered: player.parent.visible == false ? player.parent.visible=true : player.parent.visible=false
            }

            MenuItem {
                text: "Graph"
                checkable: true
                checked: graphEditor.parent.visible==true ? true : false
                onTriggered: graphEditor.parent.visible == false ? graphEditor.parent.visible=true : graphEditor.parent.visible=false
            }

            MenuItem {
                text: "Parameters"
                checkable: true
                checked: paramEditor.parent.visible==true ? true : false
                onTriggered: paramEditor.parent.visible == false ? paramEditor.parent.visible=true : paramEditor.parent.visible=false
            }*/
        }
	}
/* A revoir
        Menu {
            title: "Add"

            MenuItem {
                text: "New Node"
                onTriggered: _addMenu.showMenu(parent.x, mainMenu.height)
            }
        }
*/

    
   //this rectangle represents the zone under the menu, it allows to define the anchors.fill and margins for the SplitterRow
    Rectangle {
        id: modulsContainer
        width: parent.width
        height: parent.height - y
        color: "#353535"

        SplitView {
            anchors.fill: parent
            anchors.margins: 3
            orientation: Qt.Horizontal

            SplitView {
                id: leftColumn
                implicitWidth: 0.3 * parent.width
                implicitHeight: parent.height
                orientation: Qt.Vertical
                Layout.fillWidth: true
                Layout.minimumWidth: (topRightView.visible==true || bottomRightView.visible==true) ? 0 : parent.width

                Rectangle {
                    id: topLeftView
                    color: "#353535"
                    Layout.minimumHeight: visible ? 200 : 0
                    Layout.fillHeight: true
                    implicitWidth: parent.width

                    children:
                        switch(selectedView){
                            case 1:
                                view1[0]
                                break
                            case 2:
                                view2[0]
                                break
                            case 3:
                                view3[0]
                                break
                            default:
                                lastSelectedDefaultView[0]
                                break
                        }
                }//topLeftView

                Rectangle {
                    id: bottomLeftView
                    color: "#353535"
                    //Layout.minimumHeight: 200
                    Layout.minimumHeight: topLeftView.visible ? 200 : parent.height
                    Layout.fillHeight: true
                    implicitWidth: parent.width
                    implicitHeight: topLeftView.visible ? 0.5 * parent.height : parent.height
                    z: -1

                    children:
                        switch(selectedView){
                            case 1:
                                view1[1]
                                break
                            case 2:
                                view2[1]
                                break
                            case 3:
                                if(advancedParamEditor.displayGraph)
                                    view3[3]
                                else
                                    view3[1]
                                break
                            default:
                                lastSelectedDefaultView[1]
                                break
                        }
                }//bottomLeftView
            }//leftColumn

            SplitView {
                id: rightColumn
                implicitWidth: 0.7 * parent.width
                implicitHeight: parent.height
                orientation: Qt.Vertical
                Layout.fillWidth: true
                Layout.minimumWidth: (topLeftView.visible==true || bottomLeftView.visible==true) ? 0 : parent.width
                width : selectedView==3? 0.3*mainWindowQML.width:0.7*mainWindowQML.width

                Rectangle {
                    id: topRightView
                    color: "#353535"
                    Layout.minimumHeight: visible ? 200 : 0
                    Layout.fillHeight: true
                    implicitWidth: parent.width

                    children:
                        switch(selectedView){
                            case 1:
                                view1[2]
                                break
                            case 2:
                                view2[2]
                                break
                            case 3:
                                view3[2]
                                break
                            default:
                                lastSelectedDefaultView[2]
                                break
                        }
                }//topRightView

                Rectangle {
                    id: bottomRightView
                    color: "#353535"
                    //Layout.minimumHeight: 200
                    Layout.minimumHeight: topRightView.visible ? 200 : parent.height
                    Layout.fillHeight: true
                    implicitWidth: parent.width
                    implicitHeight: topRightView.visible ? 0.5 * parent.height : parent.height
                    z: -1
                    visible:selectedView==3? false:true

                    children:
                        switch(selectedView){
                            case 1:
                                view1[3]
                                break
                            case 2:
                                view2[3]
                                break
                            case 3:
                                view3[3]
                                break
                            default:
                                lastSelectedDefaultView[3]
                                break
                        }
                }//bottomRightView
            }//rightColumn
        }//splitview
    }//modulsContainer

    Item {
        id: subviews
        visible: false

        property variant parentBeforeFullscreen : null

        Player {
            id: player
            anchors.fill: parent
            node: _buttleData.currentViewerNodeWrapper
            onButtonCloseClicked: {
                if(parent!=fullscreenContent){
                    selectedView=-1
                    parent.visible = false
                }
                else{
                    fullscreenWindow.visibility = Window.Hidden
                    player.parent = subviews.parentBeforeFullscreen
                }
            }
            onButtonFullscreenClicked: if(parent!=fullscreenContent){subviews.parentBeforeFullscreen = parent; fullscreenWindow.visibility = Window.FullScreen; fullscreenContent.children = player}
        }

        GraphEditor {
            id: graphEditor
            anchors.fill: parent
            onButtonCloseClicked: {
                if(parent!=fullscreenContent){
                    selectedView=-1
                    parent.visible = false
                }
                else{
                    fullscreenWindow.visibility = Window.Hidden
                    graphEditor.parent = subviews.parentBeforeFullscreen
                }
            }
            onButtonFullscreenClicked: if(parent!=fullscreenContent){subviews.parentBeforeFullscreen = parent; fullscreenWindow.visibility = Window.FullScreen; fullscreenContent.children = graphEditor}
        }

        ParamTuttleEditor {
            id: paramEditor
            anchors.fill: parent
            params: _buttleData.currentParamNodeWrapper ? _buttleData.currentParamNodeWrapper.params : null
            currentParamNode: _buttleData.currentParamNodeWrapper ? _buttleData.currentParamNodeWrapper : null
            onButtonCloseClicked: {
                if(parent!=fullscreenContent){
                    selectedView=-1
                    parent.visible = false
                }
                else{
                    fullscreenWindow.visibility = Window.Hidden
                    paramEditor.parent = subviews.parentBeforeFullscreen
                }
            }
            onButtonFullscreenClicked: if(parent!=fullscreenContent){ subviews.parentBeforeFullscreen = parent; fullscreenWindow.visibility = Window.FullScreen; fullscreenContent.children = paramEditor}
        }

        ParametersEditor {
            id: advancedParamEditor
            anchors.fill: parent
            onButtonCloseClicked: {
                if(parent!=fullscreenContent){
                    selectedView=-1
                    parent.visible = false
                }
                else{
                    fullscreenWindow.visibility = Window.Hidden
                    advancedParamEditor.parent = subviews.parentBeforeFullscreen
                }
            }
            onButtonFullscreenClicked: if(parent!=fullscreenContent){subviews.parentBeforeFullscreen = parent; fullscreenWindow.visibility = Window.FullScreen; fullscreenContent.children = advancedParamEditor}
        }

        Browser {
            id: browser
            anchors.fill: parent
            onButtonCloseClicked: {
                if(parent!=fullscreenContent){
                    selectedView=-1
                    parent.visible = false
                }
                else{
                    fullscreenWindow.visibility = Window.Hidden
                    browser.parent = subviews.parentBeforeFullscreen
                }
            }

            onButtonFullscreenClicked: if(parent!=fullscreenContent){subviews.parentBeforeFullscreen = parent; fullscreenWindow.visibility = Window.FullScreen; fullscreenContent.children = browser}
        }

        Item {
            id: empty
        }

        Window {
            id: fullscreenWindow
            visibility: Window.Hidden
            visible: false
            Rectangle {
                id: fullscreenContent
                anchors.fill: parent
                color: "#353535"
            }
        }
    }
}

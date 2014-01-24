import QtQuick 2.0
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0
import QtQml 2.1
import QuickMamba 1.0
import QtQuick.Dialogs 1.0
import QtQuick.Window 2.1

import "gui/graph/qml"
import "gui/viewer/qml"
import "gui/paramEditor/qml"
import "gui/browser/qml"
import "gui/helper"

ApplicationWindow {
    property int selectedView : 1

    property variant lastSelectedDefaultView: view1
    property variant view1: [browser, paramEditor, player, graphEditor]
    property variant view2: [player, paramEditor, browser, graphEditor]
    property variant view3: [player, browser, advancedParamEditor, empty]

    width: 1200
    height: 800
    id: mainWindowQML
    title:"ButtleOFX"

    //TopFocusHandler {
    // //anchors.fill: parent
    //}

    Keys.onPressed: {

        // Graph toolbar
        if (event.key == Qt.Key_Delete) {
           _buttleManager.deleteSelection();
        }
       if ((event.key == Qt.Key_Z) && (event.modifiers & Qt.ControlModifier)) {
            if(_buttleManager.canUndo) {
                _buttleManager.undo();
            }
        }
        if ((event.key == Qt.Key_Y) && (event.modifiers & Qt.ControlModifier)) {
            if(_buttleManager.canRedo) {
                _buttleManager.redo();
            }
        }
        if ((event.key == Qt.Key_D) && (event.modifiers & Qt.ControlModifier)){
            if (!_buttleData.currentSelectedNodeWrappers.isEmpty()) {
                _buttleManager.nodeManager.duplicationNode()
            }
        }
        if ((event.key == Qt.Key_C) && (event.modifiers & Qt.ControlModifier)){
            if (!_buttleData.currentSelectedNodeWrappers.isEmpty()) {
                _buttleManager.nodeManager.copyNode()
            }
        }
        if ((event.key == Qt.Key_V) && (event.modifiers & Qt.ControlModifier)){
           if (_buttleData.canPaste) {
                _buttleManager.nodeManager.pasteNode();
           }
        }
        if ((event.key == Qt.Key_X) && (event.modifiers & Qt.ControlModifier)){
            if (!_buttleData.currentSelectedNodeWrappers.isEmpty()) {
                _buttleManager.nodeManager.cutNode()
            }
        }
        if ((event.key == Qt.Key_S) && (event.modifiers & Qt.ControlModifier)){
            if(_buttleData.graphCanBeSaved) {
                finderSaveGraph.open()
            }
        }
        if ((event.key == Qt.Key_O) && (event.modifiers & Qt.ControlModifier)){
            finderLoadGraph.open()
        }

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
        // Assign the mosquito to the selected node
        if ((event.key == Qt.Key_Return)||(event.key == Qt.Key_Enter)) {
            var selectedNodes = _buttleData.currentSelectedNodeWrappers

            // we assign the mosquito only if there is only one node selected
            if(selectedNodes.count == 1) {
                var node = selectedNodes.get(0)
                _buttleData.currentViewerNodeWrapper = node
                _buttleData.currentViewerFrame = 0
                _buttleData.assignNodeToViewerIndex(node, 0)
                _buttleEvent.emitViewerChangedSignal()
            }
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

        // Send the selected node on the parameters editor
        if ((event.key == Qt.Key_P)) {
            var selectedNodes = _buttleData.currentSelectedNodeWrappers

            // we send the node only if there is only one node selected
            if(selectedNodes.count == 1) {
                var node = selectedNodes.get(0)
                _buttleData.currentParamNodeWrapper = node
            }
        }
    }

    property bool editNode:false
    property bool docSelected:false

    //Window of hint for plugins
    PluginWindow {
        title: "Plugin's Documentation"
        visible: docSelected
        currentParamNode: _buttleData.currentParamNodeWrapper
    }

    //Node properties window

    ApplicationWindow{
        title: "Node Properties"
        visible: editNode ? true:false
        maximumHeight: 150
        maximumWidth: 280
        minimumHeight: maximumHeight
        minimumWidth: maximumWidth
        ParamButtleEditor {
            params:_buttleData.currentParamNodeWrapper ? _buttleData.currentParamNodeWrapper.params : null
            currentParamNode: _buttleData.currentParamNodeWrapper
        }
    }

    FinderLoadGraph{ id: finderLoadGraph }
    FinderSaveGraph{ id: finderSaveGraph }

    menuBar: MenuBar {
        Menu {
            title: "File"

            MenuItem {
                text: "Open"
                shortcut: "Ctrl+O"
                onTriggered: finderLoadGraph.open()
            }

            MenuItem {
                text: "Save"
                shortcut: "Ctrl+S"
                onTriggered:
                    if(_buttleData.graphCanBeSaved) {
                        finderSaveGraph.open()
                    }
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
                text: "Delete"
                shortcut: "del"
                onTriggered: _buttleManager.deleteSelection()
            }
        }
        Menu {
            id: nodesMenu
            title: "Nodes"

            Instantiator {
                model: _buttleData.pluginsIdentifiers
                MenuItem {
                    text: object
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

                        _buttleManager.nodeManager.creationNode("_buttleData.graph", object, 0, 0)
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
            }
            MenuItem {
                text: "Plugin's Documentation"
                onTriggered: docSelected=true
            }
        }


        Menu {
            title: "View"

            MenuItem {
                text: "Default"
                checkable: true
                checked: selectedView==1 ? true : false
                onTriggered: {
                    selectedView = 1
                    lastSelectedDefaultView = view1
                    topLeftView.visible=true; bottomLeftView.visible=true; topRightView.visible=true; bottomRightView.visible=true
                    rightColumn.width = 0.7*mainWindowQML.width
                }
            }

            MenuItem {
                text: "Browser Mode"
                checkable: true
                checked: selectedView==2 ? true : false
                onTriggered: {
                    selectedView = 2
                    lastSelectedDefaultView = view2
                    topLeftView.visible=true; bottomLeftView.visible=true; topRightView.visible=true; bottomRightView.visible=true
                    rightColumn.width = 0.7*mainWindowQML.width
                }
            }

            MenuItem {
                text: "Advanced Mode"
                checkable: true
                checked: selectedView==3 ? true : false
                onTriggered: {
                    selectedView = 3
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
            currentParamNode: _buttleData.currentParamNodeWrapper
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
            //Prevent browser from putting in fullscreen mode in first because of causing an OS' display bug
            onButtonFullscreenClicked: if(parent!=fullscreenContent && subviews.parentBeforeFullscreen!=null){subviews.parentBeforeFullscreen = parent; fullscreenWindow.visibility = Window.FullScreen; fullscreenContent.children = browser}
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

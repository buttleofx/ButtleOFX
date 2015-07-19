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
import "gui/browser_v2/qml"
import "gui/plugin/qml"
import "gui/shortcut/qml"

ApplicationWindow {
    property var settingsDatabase: getInitializedDatabase()

    // First, let's create a short helper function to get the database connection
    function getDatabase() {
        return LocalStorage.openDatabaseSync("ButtleOFX-settings", "2.0","ButtleOFX settings database.", 100000);
    }

    // At the start of the application, we can initialize the tables we need if they haven't been created yet
    function getInitializedDatabase() {
        var db = getDatabase();

        db.transaction(
            function(tx) {
                // Create the settings table if it doesn't already exist
                // If the table exists, this is skipped
                tx.executeSql('CREATE TABLE IF NOT EXISTS settings(key TEXT UNIQUE, value TEXT)');
            });
        return db
    }

    function saveSetting(key, value) {
        settingsDatabase.transaction( function(tx) {
            tx.executeSql('INSERT OR REPLACE INTO settings VALUES(?, ?)', [key, value]);
        });
    }

    function getSetting(key, defaultValue) {
        var res = defaultValue;

        settingsDatabase.transaction(function(tx) {
            var dbRes = tx.executeSql('SELECT value FROM settings WHERE key=?;', [key]);
            if (dbRes.rows.length > 0)
                res = dbRes.rows.item(0).value
        });
        return res;
    }

    id: mainWindowQML
    title:"ButtleOFX"
    visible: true
    width: Screen.width
    height: Screen.height

    minimumWidth: 300
    minimumHeight: 200


    property int selectedView: getSetting("view", 3)

    property variant lastSelectedView: selectedView == 1 ? view1: (selectedView == 2 ? view2 : (selectedView == 3 ? view3: view4))
    property variant view1: [browser, paramEditor, player, graphEditor]
    property variant view2: [player, paramEditor, browser, graphEditor]
    property variant view3: [player, browser, advancedParamEditor, graphEditor]
    property variant view4: view2  //just use player and browser (ie index 0&&2)

    property string urlOfFileToSave: _buttleData.urlOfFileToSave


    // TopFocusHandler {
    //     anchors.fill: parent
    // }

    Keys.onPressed: {

        // Viewer
        if ((event.key == Qt.Key_1) && (event.modifiers & Qt.KeypadModifier)) {
            player.changeViewer(1)
        }
        if ((event.key == Qt.Key_2) && (event.modifiers & Qt.KeypadModifier)) {

            player.changeViewer(2)
        }
        if ((event.key == Qt.Key_3) && (event.modifiers & Qt.KeypadModifier)) {
            player.changeViewer(3)
        }
        if ((event.key == Qt.Key_4) && (event.modifiers & Qt.KeypadModifier)) {
            player.changeViewer(4)
        }
        if ((event.key == Qt.Key_5) && (event.modifiers & Qt.KeypadModifier)) {
            player.changeViewer(5)
        }
        if ((event.key == Qt.Key_6) && (event.modifiers & Qt.KeypadModifier)) {
            player.changeViewer(6)
        }
        if ((event.key == Qt.Key_7) && (event.modifiers & Qt.KeypadModifier)) {
            player.changeViewer(7)
        }
        if ((event.key == Qt.Key_8) && (event.modifiers & Qt.KeypadModifier)) {
            player.changeViewer(8)
        }
        if ((event.key == Qt.Key_9) && (event.modifiers & Qt.KeypadModifier)) {
            player.changeViewer(9)
        }

        // Player
        if (event.key == Qt.Key_Space && player.node != null) {
            if (player.isPlaying) {
                player.doAction("pause");
            } else {
                player.doAction("play");
            }
        }
    }

    property bool aNodeIsSelected:true

    // Window of hint for plugins
    PluginWindow {
        id: doc
        title: "Plugin's Documentation"
        selectedNodeLabel: _buttleData.currentSelectedNodeWrappers.count!=0 ? _buttleData.currentSelectedNodeWrappers.get(0).name : ""
        selectedNodeDoc: _buttleData.currentSelectedNodeWrappers.count!=0 ? _buttleData.currentSelectedNodeWrappers.get(0).pluginDoc : ""
        selectedNodeGroup: _buttleData.currentSelectedNodeWrappers.count!=0 ? _buttleData.currentSelectedNodeWrappers.get(0).pluginGroup : ""
    }

    // Window of shortcuts
    ShortcutWindow {
        id: shortcuts
        title: "Shortcuts"
    }

    FileDialog {
        id: finderLoadGraph
        title: "Open a graph"
        nameFilters: [ "All files (*)" ]
        selectedNameFilter: "All files (*)"

        onAccepted: {
            if (finderLoadGraph.fileUrl) {
                _buttleData.loadData(finderLoadGraph.fileUrl)
            }
        }
    }

    FileDialog {
        id: finderSaveGraph
        title: "Save the graph"
        nameFilters:  [ "All files (*)" ]
        selectedNameFilter: "All files (*)"

        onAccepted: {
            if (finderSaveGraph.fileUrl) {
                _buttleData.saveData(finderSaveGraph.fileUrl)
            }
        }

        selectExisting: false
    }

    MessageDialog {
        id: openGraph
        title:"Save the graph?"
        icon: StandardIcon.Warning
        modality: Qt.WindowStaysOnTopHint && Qt.WindowModal
        text: urlOfFileToSave == "" ? "Save graph changes before closing ?" : "Save " + _buttleData.getFileName(urlOfFileToSave) + " changes before closing ?"
        detailedText: "If you don't save the graph, unsaved modifications will be lost. "
        standardButtons: StandardButton.Yes | StandardButton.No | StandardButton.Abort
        Component.onCompleted: visible = false

        onYes: {
            if(urlOfFileToSave!="") {
                _buttleData.saveData(urlOfFileToSave)
            } else{
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
        title: "Save the graph?"
        icon: StandardIcon.Warning
        modality: Qt.WindowStaysOnTopHint && Qt.WindowModal
        text: urlOfFileToSave == "" ? "Save graph changes before closing ?" : "Save " + _buttleData.getFileName(urlOfFileToSave) + " changes before closing ?"
        detailedText: "If you don't save the graph, unsaved modifications will be lost. "
        standardButtons: StandardButton.Yes | StandardButton.No | StandardButton.Abort
        Component.onCompleted: visible = false

        onYes: {
            if (urlOfFileToSave!="") {
                _buttleData.saveData(urlOfFileToSave)
                _buttleData.newData()
            } else {
                finderSaveGraph.open()
                _buttleData.newData()
            }
        }
        onNo: {
            _buttleData.newData()
        }
    }

    MessageDialog {
        id: closeButtle
        title: "Save the graph?"
        icon: StandardIcon.Warning
        modality: Qt.WindowStaysOnTopHint && Qt.WindowModal
        text: urlOfFileToSave == "" ? "Save graph changes before closing ?" : "Save " + _buttleData.getFileName(urlOfFileToSave) + " changes before closing ?"
        detailedText: "If you don't save the graph, unsaved modifications will be lost. "
        standardButtons: StandardButton.Yes | StandardButton.No | StandardButton.Abort
        Component.onCompleted: visible = false

        onYes: {
            if(urlOfFileToSave!="") {
                _buttleData.saveData(urlOfFileToSave)
            } else {
                finderSaveGraph.open()
                finderSaveGraph.close()
                finderSaveGraph.open()
            }
        }
        onNo: {
            Qt.quit()
        }
    }

    menuBar: MenuBar {
        Menu {
            title: "File"

            MenuItem {
                text: "New"
                shortcut: "Ctrl+N"

                onTriggered: {
                    if (!_buttleData.graphCanBeSaved) {
                        _buttleData.newData()
                    } else {
                        newGraph.open()
                    }
                }
            }

            MenuItem {
                text: "Open"
                shortcut: "Ctrl+O"

                onTriggered: {
                    if (!_buttleData.graphCanBeSaved) {
                        finderLoadGraph.open()
                    } else {
                        openGraph.open()
                        openGraph.close()
                        openGraph.open()
                    }
                }
            }

            MenuItem {
                text: "Save"
                shortcut: "Ctrl+S"
                enabled: _buttleData.graphCanBeSaved && urlOfFileToSave != "" ? true : false
                onTriggered: _buttleData.saveData(urlOfFileToSave)
            }

            MenuItem {
                text: "Save As"
                shortcut: "Ctrl+Shift+S"
                onTriggered: finderSaveGraph.open()
            }

            MenuSeparator { }

            MenuItem {
                id: quitButton
                text: "Exit"

                onTriggered: {
                    if (!_buttleData.graphCanBeSaved) {
                        Qt.quit()
                    } else {
                        closeButtle.open()
                    }
                }
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
                                if (_buttleManager.canUndo) {
                                    _buttleManager.undoNTimes(indexInStack-indexOfElement)
                                }
                            } else {
                                if (_buttleManager.canRedo) {
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
                if (_buttleManager.canUndo) {
                    _buttleManager.undo();
                }
            }

            MenuItem {
                text: "Redo"
                shortcut: "Ctrl+Y"

                onTriggered:
                if (_buttleManager.canRedo) {
                    _buttleManager.redo();
                }
            }

            MenuSeparator { }

            MenuItem {
                text: "Copy"
                shortcut: "Ctrl+C"

                onTriggered:
                if (!_buttleData.currentSelectedNodeWrappers.isEmpty()) {
                    _buttleManager.nodeManager.copyNode()
                    _buttleManager.connectionManager.copyConnections()
                }
            }

            MenuItem {
                text: "Paste"
                shortcut: "Ctrl+V"

                onTriggered:
                if (_buttleData.canPaste) {
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
                // shortcut: "del"
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
                    __parentContentItem: nodesMenu.__contentItem  // To remove warning

                    Instantiator {
                        model: _buttleData.getPluginsByPath(firstMenu.title)

                        MenuItem {
                            text: object.pluginLabel

                            onTriggered: {
                                _buttleData.setActiveGraphId("graphEditor")
                                _buttleManager.nodeManager.creationNode("graphEditor", object.pluginType, 0, 0)
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
                            __parentContentItem: nodesMenu.__contentItem  // To remove warning

                            Instantiator {
                                model: _buttleData.getPluginsByPath(secondMenu.title)

                                MenuItem {
                                    text: object.pluginLabel

                                    onTriggered: {
                                        _buttleData.setActiveGraphId("graphEditor")
                                        _buttleManager.nodeManager.creationNode("graphEditor", object.pluginType, 0, 0)
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
                                    __parentContentItem: nodesMenu.__contentItem  // To remove warning

                                    Instantiator {
                                        model: _buttleData.getPluginsByPath(thirdMenu.title)

                                        MenuItem {
                                            text: object.pluginLabel

                                            onTriggered: {
                                                _buttleData.setActiveGraphId("graphEditor")
                                                _buttleManager.nodeManager.creationNode("graphEditor", object.pluginType, 0, 0)
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
                                            __parentContentItem: nodesMenu.__contentItem  // To remove warning

                                            Instantiator {
                                                model: _buttleData.getPluginsByPath(fourthMenu.title)

                                                MenuItem {
                                                    text: object.pluginLabel

                                                    onTriggered: {
                                                        _buttleData.setActiveGraphId("graphEditor")
                                                        _buttleManager.nodeManager.creationNode("graphEditor", object.pluginType, 0, 0)
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
                                                    __parentContentItem: nodesMenu.__contentItem  // To remove warning

                                                    Instantiator {
                                                        model: _buttleData.getPluginsByPath(fifthMenu.title)

                                                        MenuItem {
                                                            text: object.pluginLabel

                                                            onTriggered: {
                                                                _buttleData.setActiveGraphId("graphEditor")
                                                                _buttleManager.nodeManager.creationNode("graphEditor", object.pluginType, 0, 0)
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
                checked: selectedView == 1

                onTriggered: {
                    selectedView = 1
                    saveSetting("view",selectedView)
                    lastSelectedView = view1
                    topLeftView.visible = true
                    bottomLeftView.visible = true
                    topRightView.visible = true
                    bottomRightView.visible = true
                    rightColumn.width = 0.7 * mainWindowQML.width
                }
            }

            MenuItem {
                id: browserView
                text: "Browser Mode"
                checkable: true
                checked: selectedView == 2

                onTriggered: {
                    selectedView = 2
                    saveSetting("view",selectedView)
                    lastSelectedView = view2
                    topLeftView.visible = true
                    bottomLeftView.visible = true
                    topRightView.visible = true
                    bottomRightView.visible = true
                    rightColumn.width = 0.7 * mainWindowQML.width
                }
            }

            MenuItem {
                id: advancedView
                text: "Quick Mode"
                checkable: true
                checked: selectedView == 3
                onTriggered: {
                    selectedView = 3
                    saveSetting("view",selectedView)
                    lastSelectedView = view3
                    topLeftView.visible=true
                    bottomLeftView.visible = true
                    topRightView.visible = true
                    bottomRightView.visible = false
                    rightColumn.width = 0.3 * mainWindowQML.width
                }
            }

            MenuItem {
                id: simpleView
                text: "Simple view"
                checkable: true
                checked: selectedView == 4

                onTriggered: {
                    selectedView = 4
                    saveSetting("view",selectedView)
                    lastSelectedView = view4
                    topLeftView.visible=true
                    topRightView.visible = true
                    bottomLeftView.visible = false
                    bottomRightView.visible = false
                    rightColumn.width = 0.7 * mainWindowQML.width
                }
            }


            /*
            MenuSeparator { }

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
            }
            */
        }
    }

    /*
    Menu {
        title: "Add"

        MenuItem {
            text: "New Node"
            onTriggered: _addMenu.showMenu(parent.x, mainMenu.height)
        }
    }
    */


    // This rectangle represents the zone under the menu, it allows to define the anchors.fill and margins for the SplitterRow
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
                Layout.minimumWidth: (topRightView.visible == true || bottomRightView.visible == true) ? 0 : parent.width

                Rectangle {
                    id: topLeftView
                    color: "#353535"
                    Layout.minimumHeight: visible ? 200 : 0
                    Layout.fillHeight: true
                    implicitWidth: parent.width
                    children: lastSelectedView[0]
                }

                Rectangle {
                    id: bottomLeftView
                    color: "#353535"
                    // Layout.minimumHeight: 200
                    Layout.minimumHeight: topLeftView.visible ? 200 : parent.height
                    Layout.fillHeight: true
                    implicitWidth: parent.width
                    implicitHeight: topLeftView.visible ? 0.5 * parent.height : parent.height
                    z: -1
                    children: selectedView != 3 ? lastSelectedView[1]: (advancedParamEditor.displayGraph? view3[3] : view3[1])
                    visible: selectedView != 4
                }
            }

            SplitView {
                id: rightColumn
                implicitWidth: 0.7 * parent.width
                implicitHeight: parent.height
                orientation: Qt.Vertical
                Layout.fillWidth: true
                Layout.minimumWidth: (topLeftView.visible == true || bottomLeftView.visible == true) ? 0 : parent.width
                width: selectedView == 3 ? 0.3 * mainWindowQML.width : 0.7 * mainWindowQML.width

                Rectangle {
                    id: topRightView
                    color: "#353535"
                    Layout.minimumHeight: visible ? 200 : 0
                    Layout.fillHeight: true
                    implicitWidth: parent.width
                    children: lastSelectedView[2]
                }

                Rectangle {
                    id: bottomRightView
                    color: "#353535"
                    // Layout.minimumHeight: 200
                    Layout.minimumHeight: topRightView.visible ? 200 : parent.height
                    Layout.fillHeight: true
                    implicitWidth: parent.width
                    implicitHeight: topRightView.visible ? 0.5 * parent.height : parent.height
                    z: -1
                    visible: selectedView == 1 || selectedView == 2
                    children: lastSelectedView[3]
                }
            }
        }
    }

    Item {
        id: subviews
        visible: false

        property variant parentBeforeFullscreen : null

        Player {
            id: player
            anchors.fill: parent
            node: _buttleData.currentViewerNodeWrapper

            onButtonCloseClicked: {
                if (parent != fullscreenContent) {
                    parent.visible = false
                } else {
                    fullscreenWindow.visibility = Window.Hidden
                    player.parent = subviews.parentBeforeFullscreen
                }
            }
            onButtonFullscreenClicked:
            if (parent != fullscreenContent){
                subviews.parentBeforeFullscreen = parent
                fullscreenWindow.visibility = Window.FullScreen
                fullscreenContent.children = player
            }
        }

        GraphEditor {
            id: graphEditor
            anchors.fill: parent

            onButtonCloseClicked: {
                if (parent!=fullscreenContent) {
                    parent.visible = false
                } else {
                    fullscreenWindow.visibility = Window.Hidden
                    graphEditor.parent = subviews.parentBeforeFullscreen
                }
            }
            onButtonFullscreenClicked:
            if (parent != fullscreenContent){
                subviews.parentBeforeFullscreen = parent
                fullscreenWindow.visibility = Window.FullScreen
                fullscreenContent.children = graphEditor
            }
        }

        ParamTuttleEditor {
            id: paramEditor
            anchors.fill: parent
            params: _buttleData.currentParamNodeWrapper ? _buttleData.currentParamNodeWrapper.params : null
            currentParamNode: _buttleData.currentParamNodeWrapper ? _buttleData.currentParamNodeWrapper : null

            onButtonCloseClicked: {
                if (parent!=fullscreenContent) {
                    parent.visible = false
                } else {
                    fullscreenWindow.visibility = Window.Hidden
                    paramEditor.parent = subviews.parentBeforeFullscreen
                }
            }
            onButtonFullscreenClicked:
            if (parent != fullscreenContent){
                subviews.parentBeforeFullscreen = parent
                fullscreenWindow.visibility = Window.FullScreen
                fullscreenContent.children = paramEditor
            }
        }

        ParametersEditor {
            id: advancedParamEditor
            anchors.fill: parent

            onButtonCloseClicked: {
                if (parent != fullscreenContent) {
                    parent.visible = false
                } else {
                    fullscreenWindow.visibility = Window.Hidden
                    advancedParamEditor.parent = subviews.parentBeforeFullscreen
                }
            }
            onButtonFullscreenClicked:
            if (parent != fullscreenContent){
                subviews.parentBeforeFullscreen = parent
                fullscreenWindow.visibility = Window.FullScreen
                fullscreenContent.children = advancedParamEditor
            }
        }

        Browser {
            id: browser
            anchors.fill: parent

            onButtonCloseClicked: {
                if (parent != fullscreenContent) {
                    selectedView =- 1
                    parent.visible = false
                } else {
                    fullscreenWindow.visibility = Window.Hidden
                    browser.parent = subviews.parentBeforeFullscreen
                }
            }
            onButtonFullscreenClicked:{
                if (parent != fullscreenContent){
                    subviews.parentBeforeFullscreen = parent
                    fullscreenWindow.visibility = Window.FullScreen
                    fullscreenContent.children = browser
                }
            }
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

import QtQuick 1.1
import QtDesktop 0.1
import QuickMamba 1.0

import "gui/graph/qml"
import "gui/viewer/qml"
import "gui/paramEditor/qml"


Item {
    Window {
        id: topLevelBrowser
        title: "ButtleOFX"
        width: 1200
        height: 800
        visible: true    

        MenuBar {
            Menu {
                text: "File"
                MenuItem {
                    text: "New"
                    shortcut: "Ctrl+N"
                    onTriggered: {
                        console.log("Salut")
                    }
                }
                MenuItem {
                    text: "Open"
                    shortcut: "Ctrl+O"
                    onTriggered: {
                    }
                }
                MenuItem {
                    text: "Save as"
                }
                MenuItem {
                    text: "Save"
                    shortcut: "Ctrl+S"
                    onTriggered: {
                        console.log("Salut")
                    }
                }

                Separator {}

                MenuItem {
                    text: "Import"
                    shortcut: "Ctrl+I"
                    onTriggered: {
                        console.log("Salut")
                    }
                }

                MenuItem {
                    text: "Export"
                    shortcut: "Ctrl+E"
                    onTriggered: {
                        console.log("Salut")
                    }
                }

                Separator {}

                MenuItem {
                    text: "Exit"
                    shortcut: "Ctrl+Q"
                    onTriggered: {
                        Qt.quit()
                    }
                }
            }

            Menu {
                text: "Edit"
                MenuItem {
                    text: "Undo"
                    shortcut: "Ctrl+Z"
                }

                MenuItem {
                    text: "Redo"
                    shortcut: "Ctrl+Y"
                }

                Separator {}

                MenuItem {
                    text: "Copy"
                    shortcut: "Ctrl + C"
                }

                MenuItem {
                    text: "Cut"
                    shortcut: "Ctrl+X"
                }

                MenuItem {
                    text: "Paste"
                    shortcut: "Ctrl+V"
                }

                MenuItem {
                    text: "Delete selection"
                }
            }

            Menu {
                text: "Add"
            }

            Menu {
                text: "Render"
                MenuItem {
                    text: "Render image"
                }

                MenuItem {
                    text: "Render animation"
                }
            }

            Menu {
                text: "Window"
                MenuItem {
                    text: "Parameters editor"
                }
                MenuItem {
                    text: "Viewer"
                }
                MenuItem {
                    text: " GraphEditor"
                }
                MenuItem {
                    text: "Tools"
                }

            }

            Menu {
                text: "Help"
                MenuItem {
                    text: "Manual"
                }
                MenuItem {
                    text: "About ButtleOFX"
                }

                Separator {}
                MenuItem {
                    text: "About Clement Champetier"
                }
            }

        }

        TopFocusHandler {
            //anchors.fill: parent
        }

        Keys.onPressed: {
            if (event.key == Qt.Key_Delete) {
                if(_buttleData.currentConnectionWrapper) {
                    _buttleManager.connectionManager.disconnect(_buttleData.currentConnectionWrapper);
                }
                else {
                    _buttleManager.nodeManager.destructionNodes();
                }
            }
            if ((event.key == Qt.Key_Z) && (event.modifiers & Qt.ControlModifier)) {
                _buttleManager.undo();
            }
            if ((event.key == Qt.Key_Y) && (event.modifiers & Qt.ControlModifier)) {
                _buttleManager.redo();
            }
            if ((event.key == Qt.Key_D) && (event.modifiers & Qt.ControlModifier)){
                _buttleManager.nodeManager.duplicationNode()
            }
            if ((event.key == Qt.Key_C) && (event.modifiers & Qt.ControlModifier)){
                _buttleManager.nodeManager.copyNode()
            }
            if ((event.key == Qt.Key_V) && (event.modifiers & Qt.ControlModifier)){
                _buttleManager.nodeManager.pasteNode()
            }
            if ((event.key == Qt.Key_X) && (event.modifiers & Qt.ControlModifier)){
                _buttleManager.nodeManager.cutNode()
            }
        }

        Rectangle {
            id: mainMenu
            width: parent.width
            height: 32
            color: "#141414"
            Row {
                spacing: 7
                x: 3
                Rectangle{
                    height: 24
                    width: 24
                    color: "#222"
                    border.width: 1
                    border.color: "#252525"
                    y: 4
                    Image {
                        id: mosquito
                        source: _buttleData.buttlePath + "/gui/img/mosquito/mosquito.png"
                        x: 2
                    }
                }
                Text {
                    color: "#00b2a1"
                    text: "ButtleOFX"
                    y: 7
                    font.pointSize: 14
                }
                /*Text {
                    color: "white"
                    text: "File"
                    y: 11
                    font.pointSize: 10

                    MouseArea {
                        anchors.fill: parent
                        hoverEnabled: true
                        onEntered: {
                            _fileMenu.showMenu(parent.x, mainMenu.height)
                        }
                    }
                }

                Text {
                    color: "white"
                    text: "Edit"
                    y: 11
                    font.pointSize: 10

                    MouseArea {
                        anchors.fill: parent
                        hoverEnabled: true
                        onEntered: {
                            _editMenu.showMenu(parent.x, mainMenu.height)
                        }
                    }
                }

                Text {
                    color: "white"
                    text: "Add"
                    y: 11
                    font.pointSize: 10

                    MouseArea {
                        anchors.fill: parent
                        hoverEnabled: true
                        onEntered: {
                            _addMenu.showMenu(parent.x, mainMenu.height)
                        }
                    }
                }

                Text {
                    color: "white"
                    text: "Render"
                    y: 11
                    font.pointSize: 10

                    MouseArea {
                        anchors.fill: parent
                        hoverEnabled: true
                        onEntered: {
                            _renderMenu.showMenu(parent.x, mainMenu.height)
                        }
                    }
                }

                Text {
                    color: "white"
                    text: "Window"
                    y: 11
                    font.pointSize: 10

                    MouseArea {
                        anchors.fill: parent
                        hoverEnabled: true
                        onEntered: {
                            _windowMenu.showMenu(parent.x, mainMenu.height)
                        }
                    }
                }

                Text {
                    color: "white"
                    text: "Help"
                    y: 11
                    font.pointSize: 10

                    MouseArea {
                        anchors.fill: parent
                        hoverEnabled: true
                        onEntered: {
                            _helpMenu.showMenu(parent.x, mainMenu.height)
                        }
                    }
                }*/

            }
        }

        //this rectangle represents the zone under the menu, it allows to define the anchors.fill and margins for the SplitterRow
        Rectangle {
            id: modulsContainer
            y: 32//mainMenu.height
            width: parent.width
            height: parent.height - y
            color: "#353535"

            SplitterRow {
                anchors.fill: parent
                anchors.margins: 3
                handleWidth: 3
 
                SplitterColumn {
                    width: 0.7*parent.width
                    height: parent.height
                    handleWidth: 3
                    //Splitter.expanding: true // obligatory to allow to have the minimumWidth

                    Player {
                        //Splitter.minimumHeight: 0
                        //Splitter.expanding: true
                        id: player
                        width: parent.width
                        height: 0.5*parent.height
                        node: _buttleData.currentViewerNodeWrapper
                    }

                    GraphEditor {
                        //Splitter.minimumHeight: 0
                        width: parent.width
                        height: 0.5*parent.height
                    }
                }

                ParamEditor {
                    //Splitter.minimumWidth: 0 
                    width: 0.3*parent.width
                    params: _buttleData.currentParamNodeWrapper ? _buttleData.currentParamNodeWrapper.params : null
                    currentParamNode: _buttleData.currentParamNodeWrapper
                }
            }
        }
    }
}

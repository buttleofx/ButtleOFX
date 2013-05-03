import QtQuick 1.1
import QtDesktop 0.1
import QuickMamba 1.0

import "gui/graph/qml"
import "gui/viewer/qml"
import "gui/paramEditor/qml"


ApplicationWindow {
        title: "ButtleOFX window" 
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
                    enabled: _buttleManager.canUndo 
                    onTriggered: _buttleManager.undo()
                }

                MenuItem {
                    text: "Redo"
                    shortcut: "Ctrl+Y"
                    enabled: _buttleManager.canRedo
                    onTriggered: _buttleManager.redo()
                }

                Separator {}

                MenuItem {
                    text: "Copy"
                    shortcut: "Ctrl+C"
                    enabled: _buttleData.currentSelectedNodeWrappers.isEmpty() ? false : true
                    onTriggered: _buttleManager.nodeManager.copyNode() 
                }

                MenuItem {
                    text: "Cut"
                    shortcut: "Ctrl+X"
                    enabled: _buttleData.currentSelectedNodeWrappers.isEmpty() ? false : true
                    onTriggered: _buttleManager.nodeManager.cutNode()

                }

                MenuItem {
                    text: "Paste"
                    shortcut: "Ctrl+V"
                    enabled: _buttleData.currentSelectedNodeWrappers.isEmpty() ? false : true
                    onTriggered: _buttleManager.nodeManager.pasteNode()
                }

                MenuItem {
                    text: "Duplicate"
                    shortcut: "Ctrl+D"
                    enabled: _buttleData.currentSelectedNodeWrappers.isEmpty() ? false : true
                    onTriggered: _buttleManager.nodeManager.duplicationNode()
                }

                MenuItem {
                    text: "Delete selection"
                    enabled: (!_buttleData.currentSelectedNodeWrappers.isEmpty() || _buttleData.currentConnectionWrapper)? true : false
                    onTriggered: {
                        if(_buttleData.currentConnectionWrapper) {
                            _buttleManager.connectionManager.disconnect(_buttleData.currentConnectionWrapper);
                        }
                        else {
                            _buttleManager.nodeManager.destructionNodes();
                        }
                    }
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

       //TopFocusHandler {
            //anchors.fill: parent
        //}

        Keys.onPressed: {
            if (event.key == Qt.Key_Delete) {
                if(_buttleData.currentConnectionWrapper) {
                    _buttleManager.connectionManager.disconnect(_buttleData.currentConnectionWrapper);
                }
                else {
                    _buttleManager.nodeManager.destructionNodes();
                }
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
            }
        }

        //this rectangle represents the zone under the menu, it allows to define the anchors.fill and margins for the SplitterRow
        Rectangle {
            id: modulsContainer
            y: mainMenu.height
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

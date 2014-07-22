import QtQuick 2.0
import QtQuick.Dialogs 1.0

import "../../plugin/qml"

Rectangle {
    id: tools

    // If the menu is open (= if "tools has children"), property children is the first list created. Else, null.
    property variant menuComponent
    property color gradian1: "#111111"
    property color gradian2: "#212121"

    signal clickCreationNode(string nodeType)

    gradient: Gradient {
        GradientStop { position: 0.0; color: gradian2 }
        GradientStop { position: 0.85; color: gradian2 }
        GradientStop { position: 0.86; color: gradian1 }
        GradientStop { position: 1; color: gradian2 }
    }

    Item {
        anchors.fill: parent
        anchors.leftMargin: 10
        anchors.topMargin: 3

        Row {
            spacing: 15
            property string imgPath: _buttleData.buttlePath + "/gui/img/buttons/tools/"

            ToolElement {
                id: plus
                imageSource: parent.imgPath + "plus.png"
                imageSourceHover: parent.imgPath + "plus_hover.png"
                imageSourceLocked: parent.imgPath + "plus.png"
                buttonName: "createNode"
                buttonText: "Create a new node"
                locked: false

                onClicked: {
                    if (pluginVisible==true){
                        pluginVisible=false
                    } else {
                        pluginVisible=true
                    }

                    editNode=false
                }
            }

            ToolElement {
                imageSource: parent.imgPath + "open.png"
                imageSourceHover: parent.imgPath + "open_hover.png"
                imageSourceLocked: parent.imgPath + "open_locked.png"
                buttonName: "load"
                buttonText: "Open a graph (Ctrl+O)"
                locked: false

                onClicked: {
                    pluginVisible=false
                    editNode=false
                    if (!_buttleData.graphCanBeSaved) {
                        finderLoadGraph.open()
                    } else {
                        openGraph.open()
                        openGraph.close()
                        openGraph.open()
                    }
                }
            }

            ToolElement {
                imageSource: parent.imgPath + "save.png"
                imageSourceHover: parent.imgPath + "save_hover.png"
                imageSourceLocked: parent.imgPath + "save_locked.png"
                buttonName: "save"
                buttonText: "Save graph (Ctrl+S)"
                locked: !_buttleData.graphCanBeSaved

                onClicked: {
                    pluginVisible=false
                    editNode=false
                    if (urlOfFileToSave!="") {
                        _buttleData.saveData(urlOfFileToSave)
                    } else {
                        finderSaveGraph.open()
                    }
                }
            }

            ToolElement {
                imageSource: parent.imgPath + "undo.png"
                imageSourceHover: parent.imgPath + "undo_hover.png"
                imageSourceLocked: parent.imgPath + "undo_locked.png"
                buttonName: "undo"
                buttonText: "Undo (Ctrl+Z)"
                locked: _buttleManager.canUndo ? false : true

                onClicked: {
                    pluginVisible=false
                    editNode=false
                    _buttleManager.undo()
                }
            }

            ToolElement {
                imageSource: parent.imgPath + "redo.png"
                imageSourceHover: parent.imgPath + "redo_hover.png"
                imageSourceLocked: parent.imgPath + "redo_locked.png"
                buttonName: "redo"
                buttonText: "Redo (Ctrl+Y)"
                locked: _buttleManager.canRedo ? false : true

                onClicked: {
                    pluginVisible=false
                    editNode=false
                    _buttleManager.redo()
                }
            }

            ToolElement {
                imageSource: parent.imgPath + "copy.png"
                imageSourceHover: parent.imgPath + "copy_hover.png"
                imageSourceLocked: parent.imgPath + "copy_locked.png"
                buttonName: "copy"
                buttonText: "Copy (Ctrl+C)"
                locked: _buttleData.currentSelectedNodeWrappers.isEmpty() ? true : false

                onClicked: {
                    pluginVisible = false
                    editNode = false
                    _buttleManager.nodeManager.copyNode()
                    _buttleManager.connectionManager.copyConnections()
                }
            }

            ToolElement {
                imageSource: parent.imgPath + "cut.png"
                imageSourceHover: parent.imgPath + "cut_hover.png"
                imageSourceLocked: parent.imgPath + "cut_locked.png"
                buttonName: "cut"
                buttonText: "Cut (Ctrl+X)"
                locked: _buttleData.currentSelectedNodeWrappers.isEmpty() ? true : false

                onClicked: {
                    pluginVisible = false
                    editNode = false
                    _buttleManager.nodeManager.cutNode()
                }
            }

            ToolElement {
                imageSource: parent.imgPath + "paste.png"
                imageSourceHover: parent.imgPath + "paste_hover.png"
                imageSourceLocked: parent.imgPath + "paste_locked.png"
                buttonName: "paste"
                buttonText: "Paste (Ctrl+V)"
                locked: _buttleData.canPaste ? false : true

                onClicked: {
                    pluginVisible = false
                    editNode = false
                    _buttleManager.nodeManager.pasteNode()
                    _buttleManager.connectionManager.pasteConnection()
                }
            }

            ToolElement {
                imageSource: parent.imgPath + "duplicate.png"
                imageSourceHover: parent.imgPath + "duplicate_hover.png"
                imageSourceLocked: parent.imgPath + "duplicate_locked.png"
                buttonName: "duplicate"
                buttonText: "Duplicate (Ctrl+D)"
                locked: _buttleData.currentSelectedNodeWrappers.isEmpty() ? true : false

                onClicked: {
                    pluginVisible = false
                    editNode = false
                    _buttleManager.nodeManager.duplicationNode()
                }
            }

            ToolElement {
                imageSource: parent.imgPath + "delete.png"
                imageSourceHover: parent.imgPath + "delete_hover.png"
                imageSourceLocked: parent.imgPath + "delete_locked.png"
                buttonName: "deleteNode"
                buttonText: "Delete the node (del)"
                locked: (!_buttleData.currentSelectedNodeWrappers.isEmpty() || _buttleData.currentConnectionWrapper) ? false : true

                onClicked: {
                    pluginVisible = false
                    editNode = false
                    _buttleManager.deleteSelection()
                }
            }

            ToolElement {
                imageSource: parent.imgPath + "center.png"
                imageSourceHover: parent.imgPath + "center_hover.png"
                imageSourceLocked: parent.imgPath + "delete_locked.png"
                buttonName: "centerGraph"
                buttonText: "Center the graph"
                locked: false

                onClicked: {
                    pluginVisible = false
                    editNode = false
                    graph.zoomCoeff = _buttleData.graphWrapper.fitInScreenSize(graph.width, graph.height).get(2)
                    graph.offsetX = (graph.container.width * 0.5 ) - (_buttleData.graphWrapper.fitInScreenSize(graph.width, graph.height).get(0) * graph.zoomCoeff)
                    graph.offsetY = (graph.container.height * 0.5 ) - (_buttleData.graphWrapper.fitInScreenSize(graph.width, graph.height).get(1) * graph.zoomCoeff)
                    miniGraph.miniOffsetX = 0
                    miniGraph.miniOffsetY = 0
                    graph.container.x = ((graph.width * 0.5) - (graph.container.width * 0.5)) + graph.offsetX - (miniGraph.miniOffsetX / miniGraph.scaleFactor *graph.zoomCoeff)
                    graph.container.y = ((graph.height * 0.5) - (graph.container.height * 0.5 )) + graph.offsetY - (miniGraph.miniOffsetY / miniGraph.scaleFactor *graph.zoomCoeff)
                }
            }
        }
    }
}

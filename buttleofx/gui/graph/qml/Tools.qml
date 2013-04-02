import QtQuick 1.1
import FolderListViewItem 1.0

Rectangle {
    id: tools
    width: 850
    height: 40

    // if the menu is open (= if "tools has children"), property children is the first list created. Else, null.
    property variant menuComponent
    property color gradian1: "#111111"
    property color gradian2: "#212121"

    signal clickCreationNode(string nodeType)

    function doAction(buttonName) {
        switch (buttonName) {
            case "createNode":
                if (!tools.menuComponent) {
                    var newComponent = Qt.createQmlObject('MenuList { parentName: "buttle/"; y: tools.height; clickFrom: tools}', parent);
                    newComponent.side = "right";
                    tools.menuComponent = newComponent;
                }
                break;

            case "deleteNode":
                if(_buttleData.currentConnectionWrapper) {
                    _buttleManager.connectionManager.disconnect(_buttleData.currentConnectionWrapper);
                }
                else {
                    _buttleManager.nodeManager.destructionNodes();
                }
                break;

            case "undo":
                _buttleManager.undo();
                break;

            case "redo":
                _buttleManager.redo();
                break;

            case "copy":
                _buttleManager.nodeManager.copyNode();
                break;

            case "paste":
                _buttleManager.nodeManager.pasteNode();
                break;

            case "cut":
                _buttleManager.nodeManager.cutNode();
                break;

            case "duplicate":
                _buttleManager.nodeManager.duplicationNode();
                break;
            default:
                break;
        }
    }

    anchors.top: parent.top
    color: "#212121"
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
                imageSource: parent.imgPath + "plus.png"
                imageSourceHover: parent.imgPath + "plus_hover.png"
                imageSourceLocked: parent.imgPath + "plus.png"
                buttonName: "createNode"
                buttonText: "Create a new node"
                locked: false
            }

            ToolElement {
                imageSource: parent.imgPath + "undo.png"
                imageSourceHover: parent.imgPath + "undo_hover.png"
                imageSourceLocked: parent.imgPath + "undo_locked.png"
                buttonName: "undo"
                buttonText: "Undo"
                locked: _buttleManager.canUndo ? false : true
            }

            ToolElement {
                imageSource: parent.imgPath + "redo.png"
                imageSourceHover: parent.imgPath + "redo_hover.png"
                imageSourceLocked: parent.imgPath + "redo_locked.png"
                buttonName: "redo"
                buttonText: "Redo"
                locked: _buttleManager.canRedo ? false : true
            }

            ToolElement {
                imageSource: parent.imgPath + "copy.png"
                imageSourceHover: parent.imgPath + "copy_hover.png"
                imageSourceLocked: parent.imgPath + "copy_locked.png"
                buttonName: "copy"
                buttonText: "Copy"
                locked: _buttleData.currentSelectedNodeWrappers.isEmpty() ? true : false
            }

            ToolElement {
                imageSource: parent.imgPath + "cut.png"
                imageSourceHover: parent.imgPath + "cut_hover.png"
                imageSourceLocked: parent.imgPath + "cut_locked.png"
                buttonName: "cut"
                buttonText: "Cut"
                locked: _buttleData.currentSelectedNodeWrappers.isEmpty() ? true : false
            }

            ToolElement {
                imageSource: parent.imgPath + "paste.png"
                imageSourceHover: parent.imgPath + "paste_hover.png"
                imageSourceLocked: parent.imgPath + "paste_locked.png"
                buttonName: "paste"
                buttonText: "Paste"
                locked: _buttleData.canPaste ? false : true
            }

            ToolElement {
                imageSource: parent.imgPath + "duplicate.png"
                imageSourceHover: parent.imgPath + "duplicate_hover.png"
                imageSourceLocked: parent.imgPath + "duplicate_locked.png"
                buttonName: "duplicate"
                buttonText: "Duplicate"
                locked: _buttleData.currentSelectedNodeWrappers.isEmpty() ? true : false
            }

            ToolElement {
                id: deleteTool
                imageSource: parent.imgPath + "delete.png"
                imageSourceHover: parent.imgPath + "delete_hover.png"
                imageSourceLocked: parent.imgPath + "delete_locked.png"
                buttonName: "deleteNode"
                buttonText: "Delete the node"
                locked: (!_buttleData.currentSelectedNodeWrappers.isEmpty() || _buttleData.currentConnectionWrapper)? false : true
            }

            // to save the graph
            Rectangle {
                id: buttonSave
                anchors.verticalCenter: parent.verticalCenter
                width: textSaveGraph.width
                height: 28
                color: "transparent"
                radius: 3

                FolderListView {
                    id: finderSaveGraph
                    typeDialog: "SaveFile"
                    messageDialog: "Save the graph"
                    directoryDialog: _buttleData.buttlePath
                }

                Text {
                    id: textSaveGraph
                    color: "#00b2a1"
                    text: "Save Graph"
                    y: 7
                    font.pointSize: 12
                }
                MouseArea {
                    hoverEnabled: true
                    anchors.fill: parent
                    onClicked: {
                        finderSaveGraph.browseFile()
                        if (finderSaveGraph.propFile) {
                            _buttleData.saveData(finderSaveGraph.propFile)
                        }
                    }
                }
            }

            // to load the graph
            Rectangle {
                id: buttonLoad
                anchors.verticalCenter: parent.verticalCenter
                width: textSaveGraph.width
                height: 28
                color: "transparent"
                radius: 3

                FolderListView {
                    id: finderLoadGraph
                    typeDialog: "OpenFile"
                    messageDialog: "Load a graph"
                    directoryDialog: _buttleData.buttlePath
                }

                Text {
                    id: textLoadGraph
                    color: "#00b2a1"
                    text: "Load Graph"
                    y: 7
                    font.pointSize: 12
                }
                MouseArea {
                    hoverEnabled: true
                    anchors.fill: parent
                    onClicked: {
                        finderLoadGraph.browseFile();
                        if (finderLoadGraph.propFile) {
                            _buttleData.loadData(finderLoadGraph.propFile)
                        }
                    }
                }
            }
        }
    }
}

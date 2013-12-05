import QtQuick 2.0
import QtQuick.Dialogs 1.0

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

                _addMenu.showMenu(parent.x , parent.y + graph.y + tools.height);
                /*if (!tools.menuComponent) {
                    var newComponent = Qt.createQmlObject('MenuList { parentName: "buttle/"; y: tools.height; clickFrom: tools}', parent);
                    newComponent.side = "right";
                    tools.menuComponent = newComponent;
                }*/
                break;

            case "deleteNode":
                _buttleManager.deleteSelection();
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

            case "save":
                finderSaveGraph.open();
                /*if (finderSaveGraph.fileUrl) {
                    _buttleData.saveData(finderSaveGraph.fileUrl)
                }*/
                break;

            case "load":
                finderLoadGraph.open();
                /*if (finderLoadGraph.fileUrl) {
                    _buttleData.loadData(finderLoadGraph.fileUrl)
                }*/
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
                id: plus
                imageSource: parent.imgPath + "plus.png"
                imageSourceHover: parent.imgPath + "plus_hover.png"
                imageSourceLocked: parent.imgPath + "plus.png"
                buttonName: "createNode"
                buttonText: "Create a new node"
                locked: false
            }

            ToolElement {

                FileDialog {
                    id: finderLoadGraph
                    title: "Open a graph"
                    folder: _buttleData.buttlePath
                    nameFilters: [ "ButtleOFX Graph files (*.bofx)", "All files (*)" ]
                    selectedNameFilter: "All files (*)"
                    onAccepted: {
                        console.log(finderLoadGraph.fileUrl)
                        _buttleData.loadData(finderLoadGraph.fileUrl)
                    }
                }

                imageSource: parent.imgPath + "open.png"
                imageSourceHover: parent.imgPath + "open_hover.png"
                imageSourceLocked: parent.imgPath + "open_locked.png"
                buttonName: "load"
                buttonText: "Open a graph (Ctrl+O)"
                locked: false
            }

            ToolElement {

                FileDialog {
                    id: finderSaveGraph
                    title: "Save the graph"
                    folder: _buttleData.buttlePath
                    nameFilters: [ "ButtleOFX Graph files (*.bofx)", "All files (*)" ]
                    selectedNameFilter: "All files (*)"
                    onAccepted: _buttleData.saveData(finderSaveGraph.fileUrl)
                }

                imageSource: parent.imgPath + "save.png"
                imageSourceHover: parent.imgPath + "save_hover.png"
                imageSourceLocked: parent.imgPath + "save_locked.png"
                buttonName: "save"
                buttonText: "Save graph (Ctrl+S)"
                locked: !_buttleData.graphCanBeSaved
            }

            ToolElement {
                imageSource: parent.imgPath + "undo.png"
                imageSourceHover: parent.imgPath + "undo_hover.png"
                imageSourceLocked: parent.imgPath + "undo_locked.png"
                buttonName: "undo"
                buttonText: "Undo (Ctrl+Z)"
                locked: _buttleManager.canUndo ? false : true
            }

            ToolElement {
                imageSource: parent.imgPath + "redo.png"
                imageSourceHover: parent.imgPath + "redo_hover.png"
                imageSourceLocked: parent.imgPath + "redo_locked.png"
                buttonName: "redo"
                buttonText: "Redo (Ctrl+Y)"
                locked: _buttleManager.canRedo ? false : true
            }

            ToolElement {
                imageSource: parent.imgPath + "copy.png"
                imageSourceHover: parent.imgPath + "copy_hover.png"
                imageSourceLocked: parent.imgPath + "copy_locked.png"
                buttonName: "copy"
                buttonText: "Copy (Ctrl+C)"
                locked: _buttleData.currentSelectedNodeWrappers.isEmpty() ? true : false
            }

            ToolElement {
                imageSource: parent.imgPath + "cut.png"
                imageSourceHover: parent.imgPath + "cut_hover.png"
                imageSourceLocked: parent.imgPath + "cut_locked.png"
                buttonName: "cut"
                buttonText: "Cut (Ctrl+X)"
                locked: _buttleData.currentSelectedNodeWrappers.isEmpty() ? true : false
            }

            ToolElement {
                imageSource: parent.imgPath + "paste.png"
                imageSourceHover: parent.imgPath + "paste_hover.png"
                imageSourceLocked: parent.imgPath + "paste_locked.png"
                buttonName: "paste"
                buttonText: "Paste (Ctrl+V)"
                locked: _buttleData.canPaste ? false : true
            }

            ToolElement {
                imageSource: parent.imgPath + "duplicate.png"
                imageSourceHover: parent.imgPath + "duplicate_hover.png"
                imageSourceLocked: parent.imgPath + "duplicate_locked.png"
                buttonName: "duplicate"
                buttonText: "Duplicate (Ctrl+D)"
                locked: _buttleData.currentSelectedNodeWrappers.isEmpty() ? true : false
            }

            ToolElement {
                imageSource: parent.imgPath + "delete.png"
                imageSourceHover: parent.imgPath + "delete_hover.png"
                imageSourceLocked: parent.imgPath + "delete_locked.png"
                buttonName: "deleteNode"
                buttonText: "Delete the node (suppr)"
                locked: (!_buttleData.currentSelectedNodeWrappers.isEmpty() || _buttleData.currentConnectionWrapper)? false : true
            }            
        }
    }
}

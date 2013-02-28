import QtQuick 1.1

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
                    var newComponent = Qt.createQmlObject('MenuList { parentName: "buttle/"; y: tools.height;}', parent);
                    tools.menuComponent = newComponent;
                }
                break;

            case "deleteNode":
                _buttleManager.destructionNodes();
                break;

            case "undo":
                _buttleManager.undo();
                break;

            case "redo":
                _buttleManager.redo();
                break;

            case "copy":
                _buttleManager.copyNode();
                break;

            case "paste":
                _buttleManager.pasteNode();
                break;

            case "cut":
                _buttleManager.cutNode();
                break;

            case "duplicate":
                _buttleManager.duplicationNode();
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

            ToolElement {
                imageSource: "img/buttons/plus.png"
                imageSourceHover: "img/buttons/plus_hover.png"
                imageSourceLocked: "img/buttons/plus.png"
                buttonName: "createNode"
                buttonText: "Create a new node"
                locked: false
            }

            ToolElement {
                imageSource: "img/buttons/undo.png"
                imageSourceHover: "img/buttons/undo_hover.png"
                imageSourceLocked: "img/buttons/undo_locked.png"
                buttonName: "undo"
                buttonText: "Undo"
                locked: _buttleManager.canUndo ? false : true
            }

            ToolElement {
                imageSource: "img/buttons/redo.png"
                imageSourceHover: "img/buttons/redo_hover.png"
                imageSourceLocked: "img/buttons/redo_locked.png"
                buttonName: "redo"
                buttonText: "Redo"
                locked: _buttleManager.canRedo ? false : true
            }

            ToolElement {
                imageSource: "img/buttons/copy.png"
                imageSourceHover: "img/buttons/copy_hover.png"
                imageSourceLocked: "img/buttons/copy_locked.png"
                buttonName: "copy"
                buttonText: "Copy"
                locked: _buttleData.currentSelectedNodeWrapper ? false : true
            }

            ToolElement {
                imageSource: "img/buttons/cut.png"
                imageSourceHover: "img/buttons/cut_hover.png"
                imageSourceLocked: "img/buttons/cut_locked.png"
                buttonName: "cut"
                buttonText: "Cut"
                locked: _buttleData.currentSelectedNodeWrapper ? false : true
            }

            ToolElement {
                imageSource: "img/buttons/paste.png"
                imageSourceHover: "img/buttons/paste_hover.png"
                imageSourceLocked: "img/buttons/paste_locked.png"
                buttonName: "paste"
                buttonText: "Paste"
                locked: _buttleData.canPaste ? false : true
            }

            ToolElement {
                imageSource: "img/buttons/duplicate.png"
                imageSourceHover: "img/buttons/duplicate_hover.png"
                imageSourceLocked: "img/buttons/duplicate_locked.png"
                buttonName: "duplicate"
                buttonText: "Duplicate"
                locked: _buttleData.currentSelectedNodeWrapper ? false : true
            }

            ToolElement {
                id: deleteTool
                imageSource: "img/buttons/delete.png"
                imageSourceHover: "img/buttons/delete_hover.png"
                imageSourceLocked: "img/buttons/delete_locked.png"
                buttonName: "deleteNode"
                buttonText: "Delete the node"
                locked: _buttleData.currentSelectedNodeWrapper ? false : true

            }
        }
    }
}

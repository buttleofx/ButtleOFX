import QtQuick 1.1

Rectangle {
    id: tools
    width: 850
    height: 40

    // if the menu is open (= if "tools has children"), property children is the first list created. Else, null.
    property variant children
    property color gradian1: "#111111"
    property color gradian2: "#212121"

    property int buttonSize : 20

    signal clickCreationNode(string nodeType)

    function doAction(buttonName) {
        switch (buttonName) {
            case "createNode":
                var newComponent = Qt.createQmlObject('MenuList { parentName: "buttle/"; y: tools.height;}', parent);
                tools.children = newComponent;
                break;

            case "deleteNode":
                _buttleData.destructionNode();
                break;

            case "undo":
                _buttleData.undo();
                break;

            case "redo":
                _buttleData.redo();
                break;

            case "copy":
                _buttleData.copyNode();
                break;

            case "paste":
                _buttleData.pasteNode();
                break;

            case "cut":
                _buttleData.cutNode();
                break;

            case "duplicate":
                _buttleData.duplicateNode();
                break;
            default:
                break;
        }
    }

    z: 2000
    anchors.top: parent.top
    color: "#212121"
    gradient: Gradient {
        GradientStop { position: 0.0; color: gradian2 }
        GradientStop { position: 0.85; color: gradian2 }
        GradientStop { position: 0.86; color: gradian1 }
        GradientStop { position: 1; color: gradian2 }
    }

    // On mouse entered the tools area, we destroy the MenuList component if it exists.
    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        onEntered: {
            if (tools.children) {
                tools.children.destroy();
            }
        }
    }

    Item {
        anchors.fill: parent

        ListModel {
            id: modelButtonsTools
            ListElement { imageSource: "img/buttons/cut.png"; buttonName: "createNode"; text: "Create a new node"; }
            ListElement { imageSource: "img/buttons/undo.png"; buttonName: "undo"; text: "Undo"; }
            ListElement { imageSource: "img/buttons/redo.png"; buttonName: "redo"; text: "redo"; }
            ListElement { imageSource: "img/buttons/copy.png"; buttonName: "copy"; text: "Copy"; }
            ListElement { imageSource: "img/buttons/cut.png"; buttonName: "cut"; text: "Cut"; }
            ListElement { imageSource: "img/buttons/past.png"; buttonName: "past"; text: "Paste"; }
            ListElement { imageSource: "img/buttons/duplicate.png"; buttonName: "duplicate"; text: "Duplicate"; }
            ListElement { imageSource: "img/buttons/cut.png"; buttonName: "deleteNode"; text: "Delete the node"; }
        }

        ListView {
            anchors.fill: parent
            model: modelButtonsTools
            orientation: ListView.Horizontal
            spacing: 15
            delegate {
                Component {
                    id: buttonTools
                    Rectangle {
                        id: undoButton
                        anchors.verticalCenter: parent.verticalCenter
                        implicitWidth: buttonSize
                        implicitHeight: buttonSize
                        color: "transparent"
                        Image {
                            source: imageSource
                            anchors.verticalCenter: parent.verticalCenter
                        }
                        MouseArea {
                            anchors.fill: parent
                            onClicked: tools.doAction(buttonName);
                        }
                    }
                }
            }
        }
    }
}



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
                _buttleData.duplicationNode();
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

        ListModel {
            id: modelButtonsTools
            ListElement { imageSource: "img/buttons/cut.png"; buttonName: "createNode"; buttonText: "Create a new node"; }
            ListElement { imageSource: "img/buttons/undo.png"; buttonName: "undo"; buttonText: "Undo"; }
            ListElement { imageSource: "img/buttons/redo.png"; buttonName: "redo"; buttonText: "Redo"; }
            ListElement { imageSource: "img/buttons/copy.png"; buttonName: "copy"; buttonText: "Copy"; }
            ListElement { imageSource: "img/buttons/cut.png"; buttonName: "cut"; buttonText: "Cut"; }
            ListElement { imageSource: "img/buttons/past.png"; buttonName: "paste"; buttonText: "Paste"; }
            ListElement { imageSource: "img/buttons/duplicate.png"; buttonName: "duplicate"; buttonText: "Duplicate"; }
            ListElement { imageSource: "img/buttons/cut.png"; buttonName: "deleteNode"; buttonText: "Delete the node"; }
        }

        ListView {
            anchors.fill: parent
            anchors.leftMargin: 10
            anchors.topMargin: -5
            model: modelButtonsTools
            orientation: ListView.Horizontal
            spacing: 15
            interactive: false
            delegate {
                Component {
                    Rectangle {
                        id: buttonTools
                        anchors.verticalCenter: parent.verticalCenter
                        width: 26
                        height: 26
                        color: "transparent"
                        state: "normal"
                        radius: 3
                        Image {
                            source: imageSource
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.horizontalCenter: parent.horizontalCenter
                        }
                        MouseArea {
                            id: buttonMouseArea
                            hoverEnabled: true
                            anchors.fill: parent
                            onClicked: tools.doAction(buttonName);
                        }
                        Rectangle {
                            id: infoTools
                            x: 15
                            y: 35
                            color: "grey"
                            opacity: buttonMouseArea.containsMouse ? 1 : 0
                            Text {
                                text: buttonText
                                color: "#bbbbbb"
                            }
                        }

                        StateGroup {
                            id: stateButtonEvents
                             states: [
                                 State {
                                     name: "normal"
                                     when: !buttonMouseArea.containsMouse
                                     PropertyChanges {
                                         target: buttonTools
                                         color:  "transparent"
                                     }
                                 },
                                 State {
                                     name: "pressed"
                                     when: buttonMouseArea.containsMouse && buttonMouseArea.pressed
                                     PropertyChanges {
                                         target: buttonTools;
                                         color:  "#00b2a1"
                                     }
                                 },
                                 State {
                                     name: "hover"
                                     when: buttonMouseArea.containsMouse
                                     PropertyChanges {
                                         target: buttonTools;
                                         color:  "#555555"
                                     }
                                 }

                             ]
                        }
                    }
                }
            }
        }
    }
}



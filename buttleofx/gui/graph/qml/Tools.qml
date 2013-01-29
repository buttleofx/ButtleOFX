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

    Row {
        spacing: 15
        y: 5
        // create and delete node
        Rectangle {
            id: addNodeButton
            anchors.verticalCenter: parent.verticalCenter
            implicitWidth: buttonSize
            implicitHeight: buttonSize
            width: 7/10 * tools.height
            height: width
            color: "transparent"
            Text {
                anchors.centerIn: parent
                text: "+"
                font.pointSize: 16
                color: "white"
            }
            MouseArea {
                anchors.fill: parent

                // On clicked, we create a MenuList component and add it to the tools' children.
                onClicked: {
                    var newComponent = Qt.createQmlObject('MenuList { parentName: "buttle/"; y: 30;}', parent);
                    tools.children = newComponent;
                }
            }
        }

        Rectangle {
            id: delNodeButton
            anchors.verticalCenter: parent.verticalCenter
            implicitWidth: buttonSize
            implicitHeight: buttonSize
            width: 7/10 * tools.height
            height: width
            color: "transparent"
            Text {
                anchors.centerIn: parent
                text: "-"
                font.pointSize: 16
                color: "white"
            }
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    _buttleData.destructionNode()
                }
            }
        }

        // undo redo
        Rectangle {
            id: undoButton
            anchors.verticalCenter: parent.verticalCenter
            implicitWidth: buttonSize
            implicitHeight: buttonSize
            width: 4/10 * tools.height
            height: width
            color: "transparent"
            Image {
                source: "img/buttons/undo.png"
                anchors.verticalCenter: parent.verticalCenter
            }
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    _buttleData.undo();
                }
            }
        }

        Rectangle {
            id: redoButton
            anchors.verticalCenter: parent.verticalCenter
            implicitWidth: buttonSize
            implicitHeight: buttonSize
            width: 4/10 * tools.height
            height: width
            color: "transparent"
            Image {
                source: "img/buttons/redo.png"
                anchors.verticalCenter: parent.verticalCenter
            }
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    _buttleData.redo();
                }
            }
        }

        // copy / cut / past / duplicate
        Rectangle {
            id: copyButton
            anchors.verticalCenter: parent.verticalCenter
            implicitWidth: buttonSize
            implicitHeight: buttonSize
            width: 4/10 * tools.height
            height: width
            color: "transparent"
            Image {
                source: "img/buttons/copy.png"
                anchors.verticalCenter: parent.verticalCenter
            }
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    _buttleData.copyNode();
                }
            }
        }

        Rectangle {
            id: cutButton
            anchors.verticalCenter: parent.verticalCenter
            implicitWidth: buttonSize
            implicitHeight: buttonSize
            width: 4/10 * tools.height
            height: width
            color: "transparent"
            Image {
                source: "img/buttons/cut.png"
                anchors.verticalCenter: parent.verticalCenter
            }
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    _buttleData.cutNode();
                }
            }
        }

        Rectangle {
            id: pastButton
            anchors.verticalCenter: parent.verticalCenter
            implicitWidth: buttonSize
            implicitHeight: buttonSize
            width: 4/10 * tools.height
            height: width
            color: "transparent"
            Image {
                source: "img/buttons/past.png"
                anchors.verticalCenter: parent.verticalCenter
            }
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    _buttleData.pasteNode();
                }
            }
        }

        Rectangle {
            id: duplicateButton
            anchors.verticalCenter: parent.verticalCenter
            implicitWidth: buttonSize
            implicitHeight: buttonSize
            width: 4/10 * tools.height
            height: width
            color: "transparent"
            Image {
                source: "img/buttons/duplicate.png"
                anchors.verticalCenter: parent.verticalCenter
            }
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    _buttleData.duplicationNode();
                }
            }
        }
    }
}



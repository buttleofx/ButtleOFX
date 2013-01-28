import QtQuick 1.1

Rectangle {
    id: tools
    width: 850
    height: 30

    // if the menu is open (= if "tools has children"), property children is the first list created. Else, null.
    property variant children

    signal clickCreationNode(string nodeType)

    z: 2000
    anchors.top: parent.top
    color: "#212121"

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

    Rectangle {
        id: addNodeButton
        implicitWidth: 20
        implicitHeight: 20
        width: 7/10 * parent.height
        height: width
        anchors.verticalCenter: parent.verticalCenter
        color: "#212121"
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
                var newComponent = Qt.createQmlObject('MenuList { parentName: "tuttle/"; y: 30;}', parent);
                tools.children = newComponent;
            }
        }
    }

    Rectangle {
        id: delNodeButton
        implicitWidth: 20
        implicitHeight: 20
        width: 7/10 * parent.height
        height: width
        x: 30
        y: 6
        color: "#212121"
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

    Rectangle {
        id: undoButton
        implicitWidth: 20
        implicitHeight: 20
        width: 7/10 * parent.height
        height: width
        x: 80
        y: 10
        color: "#212121"
        Image {
            source: "img/buttons/undo.png"
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
        implicitWidth: 20
        implicitHeight: 20
        width: 7/10 * parent.height
        height: width
        x: 110
        y: 10
        color: "#212121"
        Image {
            source: "img/buttons/redo.png"
        }
        MouseArea {
            anchors.fill: parent
            onClicked: {
                _buttleData.redo();
            }
        }
    }

}

import QtQuick 1.1

Rectangle {
    id: tools
    width: 850
    height: 30
    property variant children

    signal clickCreationNode(string nodeType)

    z: 2000
    anchors.top: parent.top
    color: "#212121"

    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        onEntered: {
            if (tools.children) {
                console.log("has children")
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

}

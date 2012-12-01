import Qt 4.7

Rectangle {
    id: tools
    width: parent.width
    height: 30
    anchors.top: parent.top
    color: "#212121"
    Rectangle {
        id: addNodeButton
        width: 20
        height: 20
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
                console.log("Add Node");
                addNode();
            }
        }
    }
    Rectangle {
        id: delNodeButton
        width: 20
        height: 20
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
                console.log("Delete Node");
                deleteNode(nodeSelected);
            }
        }
    }
}

import Qt 4.7

Rectangle {
    id: node
    property int number
    signal deleteNode (int index)
    height: 40
    width: 110
    x: 10
    y: 40
    color: "transparent"

    Keys.onPressed: {
            if (event.key==Qt.Key_Delete) {
                if (node.focus == true){
                    console.log("Suppression noeud " + number);
                    deleteNode(number);
                }
            }
        }

    Rectangle {
        id: nodeBorder
        height: node.height
        width: node.width
        anchors.centerIn: parent
        color: "#aaaaaa"
        opacity: 0.5
        radius: 10
    }
    Rectangle {
        id: nodeRectangle
        anchors.centerIn: parent
        height: node.height - 8
        width: node.width - 8
        color: "#bbbbbb"
        radius: 8
        Text {
            anchors.centerIn: parent
            text: "Node"
            font.pointSize: 10
            color: "black"
        }
    }
    Column {
        id: nodeInputs
        anchors.horizontalCenter: parent.left
        anchors.top: parent.verticalCenter
        spacing: 2
        property int nbInputs: 2
        Repeater {
            model: nodeInputs.nbInputs
            Rectangle {
                height: 5
                width: 5
                color: "#bbbbbb"
                radius: 2
            }
        }
    }
    Column {
        id: nodeOutputs
        anchors.horizontalCenter: parent.right
        anchors.top: parent.verticalCenter
        spacing: 2
        Repeater {
            model: 1
            Rectangle {
                height: 5
                width: 5
                color: "#bbbbbb"
                radius: 2
                MouseArea {
                    anchors.fill: parent
                }
            }
        }
    }
    states: State {
        name: "selected";
        when: node.focus
        PropertyChanges {
            target: nodeRectangle
            color: "#d9d9d9"
        }
    }
    MouseArea {
        anchors.fill: parent
        drag.target: parent
        drag.axis: Drag.XandYAxis
        onPressed: {
            node.focus = true
            parent.opacity = 0.5
            nodeSelected = number
        }
        onReleased: {
            parent.opacity = 1
        }
        onClicked: {
            //node.focus = true
            nodeSelected = parent.number
            console.log(parent.number)
        }
    }
    
}

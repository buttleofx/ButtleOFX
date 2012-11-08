import Qt 4.7

Rectangle {
    id: node
    height: 40
    width: 110
    x: model.element.nodeXCoord
    y: model.element.nodeYCoord
    color: "transparent"
    Rectangle {
        id: nodeBorder
        height: 40
        width: 110
        anchors.centerIn: parent
        color: model.element.nodeColor
        opacity: 0.5
        radius: 10
    }
    Rectangle {
        id: nodeRectangle
        anchors.centerIn: parent
        height: 32
        width: 102
        color: "#bbbbbb"
        radius: 8
        Text {
            anchors.centerIn: parent
            text: model.element.nodeName
            font.pointSize: 10
            color: "black"
        }
    }
    Column {
        id: nodeInputs
        anchors.horizontalCenter: parent.left
        anchors.top: parent.verticalCenter
        spacing: 2
        property int nbInputs: model.element.nodeNbInput
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
    MouseArea {
        anchors.fill: parent
        drag.target: parent
        drag.axis: Drag.XandYAxis
        onPressed: parent.opacity = 0.5
        onReleased: {
            parent.opacity = 1;
            console.log(parent.x)
            console.log(parent.y)
            model.element.nodeXCoord = parent.x
            model.element.nodeYCoord = parent.y
        }
        onClicked: {
            console.log(model.element.nodeName)
        }
    }
}

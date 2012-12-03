import QtQuick 1.1

Item {
    id: node
    property int number
    signal deleteNode (int index)
    height: 40
    width: 110
    x: _nodeManager.getWrapper(node).nodeXCoord
    y: _nodeManager.getWrapper(node).nodeYCoord
    focus: _nodeManager.currentNode == node

    Keys.onPressed: {
            if (event.key==Qt.Key_Delete) {
                if (node.focus == true){
                    console.log("Suppression noeud " + number);
                    //deleteNode(number);
                    _nodeManager.deleteNode(node)
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
            text: _nodeManager.getWrapper(node).nodeName
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
//            nodeSelected = number
            _nodeManager.currentNode = node;
        }
        onReleased: {
            parent.opacity = 1
        }
        onClicked: {
            //node.focus = true
//            _nodeManager.currentNode = node;
//            nodeSelected = parent.number
//            console.log(parent.number)
        }
    }
    
}

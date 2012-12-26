import QtQuick 1.1

import Qt 4.7

Rectangle {
    id: node
    property variant nodeModel : model.object
    height: 35 + 7*nodeModel.nbInput
    width: 110
    x: nodeModel.coord[0]
    y: nodeModel.coord[1]
    color: "transparent"
    focus: true

    Keys.onPressed: {
        if (event.key == Qt.Key_Delete) {
            console.log("destruction");
            _graphWrapper.destructionProcess();
        }
    }

    Rectangle {
        id: nodeBorder
        height: 40
        width: 110
        anchors.centerIn: parent
        color: nodeModel.color
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
            text: nodeModel.name
            font.pointSize: 10
            color: (nodeModel.name === _graphWrapper.currentNode) ? "#00b2a1" : "black"
        }
    }
    Column {
        id: nodeInputs
        anchors.horizontalCenter: parent.left
        anchors.top: parent.verticalCenter
        spacing: 2
        property int nbInput: nodeModel.nbInput
        property string port : "input"
        Repeater {
            model: nodeInputs.nbInput
            Clip {}
        }
    }
    Column {
        id: nodeOutputs
        anchors.horizontalCenter: parent.right
        anchors.top: parent.verticalCenter
        spacing: 2
        property string port : "output"
        Repeater {
            model: 1
            Clip {}
        }
    }
    MouseArea {
        anchors.fill: parent
        drag.target: parent
        drag.axis: Drag.XandYAxis
        onPressed: parent.opacity = 0.5
        onReleased: {
            parent.opacity = 1;
            nodeModel.nodeMoved(parent.x, parent.y)
        }
        onClicked: {
            console.log(nodeModel.name)
            _graphWrapper.setCurrentNode(nodeModel.name)
        }
    }
}




/*Item {
    id: node

    height: 35 + 7*_graphWrapper.getWrappers(node).nbInput
    width: 110
    x: _graphWrapper.getWrappers(node).x
    y: _graphWrapper.getWrappers(node).y
    z: _graphWrapper.getZMax()
    focus: true

    Keys.onPressed: {
            if (event.key == Qt.Key_Delete) {
                    _graphWrapper.deleteCurrentNode()
            }
    }

    Rectangle {
        id: nodeBorder
        height: node.height
        width: node.width
        anchors.centerIn: parent
        color: _graphWrapper.getWrappers(node).color
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
            id: nodeName
            anchors.centerIn: parent
            text: _graphWrapper.getWrappers(node).name
            font.pointSize: 10
            color: "black"
        }
    }
    Column {
        id: nodeInputs
        anchors.horizontalCenter: parent.left
        anchors.verticalCenter: parent.verticalCenter
        spacing: 2
        Repeater {
            model: _graphWrapper.getWrappers(node).nbInput
            Rectangle {
                id: nodeInput
                height: 5
                width: 5
                color: "#bbbbbb"
                radius: 2
                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    onPressed: {
                        color = "red"
                        console.log("Input clicked");
                        _connectionManager.inputPressed(nodeName.text, "in" + index) // we send the node name and the id of the input
                    }
                    onReleased: {
                        color = "#bbbbbb"
                        _connectionManager.inputReleased(nodeName.text, "in" + index)
                    }
                    onEntered: {
                        color = "blue"
                    }
                    onExited: {
                        color = "#bbbbbb"
                    }
                }
            }
        }
    }
    Column {
        id: nodeOutput
        anchors.horizontalCenter: parent.right
        anchors.verticalCenter: parent.verticalCenter
        spacing: 2

        Repeater {
            model: 1
            Rectangle {
                id: nodeOutput
                height: 5
                width: 5
                color: "#bbbbbb"
                radius: 2
                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    onPressed: {
                        color = "red"
                        console.log("Output clicked");
                        _connectionManager.outputPressed(nodeName.text, "out" + index)
                    }
                    onReleased: {
                        color = "#bbbbbb"
                        _connectionManager.outputReleased(nodeName.text, "out" + index)
                    }
                    onEntered: {
                        color = "blue"
                    }
                    onExited: {
                        color = "#bbbbbb"
                    }
                }
            }
        }
    }
    states: State {
        name: "selected";
        when: _graphWrapper.currentNode == node
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
            _graphWrapper.currentNode = node
            parent.opacity = 0.5
            if(_graphWrapper.currentNode != node) {
                _graphWrapper.setZMax()
                parent.z = _graphWrapper.getZMax()
                console.log(parent.z)
            }

        }
        onReleased: {
            parent.opacity = 1
        }
    }
}*/

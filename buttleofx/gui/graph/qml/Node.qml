import QtQuick 1.1

import Qt 4.7

Rectangle {
    id: node

    QtObject {
        id: m
        property variant nodeModel: model.object
    }
    property int heightEmptyNode : 35
    property int nbInput: m.nodeModel.nbInput

    height: node.heightEmptyNode + node.inputSpacing * node.nbInput
    width: 110

    property int inputSpacing : 7
    property int clipSize: 8
    property int inputTopMargin: (node.height- node.clipSize*node.nbInput - node.inputSpacing * (node.nbInput-1)) / 2
    property int inputSideMargin: 6

    z: _graphWrapper.getZMax()
    color: "transparent"
    focus: true

    Rectangle {
        id: nodeBorder
        height: parent.height
        width: 110
        anchors.centerIn: parent
        color: m.nodeModel.color
        opacity: 0.5
        radius: 10
    }
    Rectangle {
        id: nodeRectangle
        anchors.centerIn: parent
        height: parent.height - 8
        width: 102
        color: "#bbbbbb"
        radius: 8
        Text {
            anchors.centerIn: parent
            text: m.nodeModel.name
            font.pointSize: 10
            color: (m.nodeModel.name == _graphWrapper.currentNode) ? "#00b2a1" : "black"
        }
    }
    Column {
        id: nodeInputs
        anchors.left: parent.left
        anchors.leftMargin: -node.inputSideMargin
        anchors.top: parent.top
        anchors.topMargin: node.inputTopMargin
        spacing: node.inputSpacing
        property string port : "input"
        Repeater {
            model: node.nbInput
            Clip {}
        }
    }
    Column {
        id: nodeOutputs
        anchors.right: parent.right
        anchors.rightMargin: -node.inputSideMargin
        anchors.top: parent.verticalCenter
        spacing: 2
        property string port : "output"
        Repeater {
            model: 1
            Clip {
            }
        }
    }

    StateGroup {
        id: stateMoving
        state: "normal"
        states: [
            State {
                name: "normal"
                PropertyChanges { target: node; x: m.nodeModel.coord[0]; y: m.nodeModel.coord[1] }
            },
            State {
                name: "moving"
                PropertyChanges { target: node; x: m.nodeModel.coord[0] ; y: m.nodeModel.coord[1] }
            }
        ]
    }

    StateGroup {
        id: statePressed
        states: [
            State {
            name: "pressed"
            when: nodeMouseArea.pressed
            PropertyChanges { target: node; opacity: .5 }
            }
        ]
    }

    MouseArea {
        id: nodeMouseArea
        anchors.fill: parent
        drag.target: parent
        drag.axis: Drag.XandYAxis
        onPressed: {
            console.log("node onPressed")
            if(_graphWrapper.getCurrentNode() != m.nodeModel.name) {
                _graphWrapper.setCurrentNode(m.nodeModel.name)
                _graphWrapper.setZMax()
                parent.z = _graphWrapper.getZMax()
            }
            stateMoving.state = "moving"
        }
        onReleased: {
            console.log("node onReleased")
            m.nodeModel.nodeMoved(parent.x, parent.y, _cmdManager)
            stateMoving.state = "normal"
            //m.modelPosX = nodeModel.coord[0]
            //m.modelPosY = nodeModel.coord[1]
            console.log(m.nodeModel.coord[0])
            console.log(m.nodeModel.coord[1])
        }
    }
}

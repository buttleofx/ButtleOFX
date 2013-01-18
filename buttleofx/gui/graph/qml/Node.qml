import QtQuick 1.1


Rectangle {
    id: node

    QtObject {
        id: m
        property variant nodeModel: model.object
    }
    property int heightEmptyNode : _buttleData.graphWrapper.heightEmptyNode
    property int nbInput: m.nodeModel.nbInput

    height: node.heightEmptyNode + node.inputSpacing * node.nbInput
    width: 110

    property int inputSpacing : _buttleData.graphWrapper.clipSpacing
    property int clipSize: _buttleData.graphWrapper.clipSize

    x: m.nodeModel.coord[0]
    y: m.nodeModel.coord[1]
    z: _buttleData.graphWrapper.zMax

    property int inputTopMargin: (node.height- node.clipSize*node.nbInput - node.inputSpacing * (node.nbInput-1)) / 2
    property int inputSideMargin: _buttleData.graphWrapper.nodeInputSideMargin

    color: "transparent"
    focus: true

    Rectangle {
        id: nodeBorder
        height: parent.height
        width: _buttleData.graphWrapper.widthNode
        anchors.centerIn: parent
        color: m.nodeModel.color
        opacity: 0.5
        radius: 10
    }
    Rectangle {
        id: nodeRectangle
        anchors.centerIn: parent
        height: parent.height - 8
        width: nodeBorder.width - 10
        color: "#bbbbbb"
        radius: 8
        Text {
            anchors.centerIn: parent
            text: m.nodeModel.name
            font.pointSize: 10
            color: (m.nodeModel == _buttleData.graphWrapper.currentNodeWrapper) ? "#00b2a1" : "black"
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
            if(_buttleData.graphWrapper.currentNodeWrapper != m.nodeModel) {
                _buttleData.graphWrapper.currentNodeWrapper = m.nodeModel
                _buttleData.graphWrapper.zMax += 1
                parent.z = _buttleData.graphWrapper.zMax
            }
            stateMoving.state = "moving"
            _buttleData.graphWrapper.updateConnectionsCoord()
        }
        onReleased: {
            console.log("node onReleased")

           // m.nodeModel.nodeMoved(parent.x, parent.y) // (obsolete)
            _buttleData.graphWrapper.nodeMoved(m.nodeModel.name, parent.x, parent.y)
            /*
                => Why not managed by the nodeWrapped anymore ? Because we can't store the node in the cmdManager, we need to store the node name.
                If we store the node and the node is deleted, we won't be able to apply undo/redo on it because the recreated node won't be the same.
                But the node name will be the same. So we need the node name.
                The fonction is managed by the graphWrapper because in order to find the right node, we need to give the graph to the cmdManager.
            */

            stateMoving.state = "normal"
            //m.modelPosX = nodeModel.coord[0]
            //m.modelPosY = nodeModel.coord[1]
            console.log(m.nodeModel.coord[0])
            console.log(m.nodeModel.coord[1])
            _buttleData.graphWrapper.updateConnectionsCoord()
        }
    }
}

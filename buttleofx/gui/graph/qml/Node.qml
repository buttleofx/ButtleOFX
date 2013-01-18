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

    x: m.nodeModel.coord.x
    y: m.nodeModel.coord.y
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
            color: (m.nodeModel == _buttleData.graphWrapper.currentSelectedNodeWrapper) ? "#00b2a1" : "black"
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
                PropertyChanges { target: node; x: m.nodeModel.coord.x; y: m.nodeModel.coord.y }
            },
            State {
                name: "moving"
                PropertyChanges { target: node; x: m.nodeModel.coord.x ; y: m.nodeModel.coord.y }
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
        acceptedButtons: Qt.LeftButton | Qt.RightButton
        onPressed: {
            // left button : we change the current selected node & we start moving
            if (mouse.button == Qt.LeftButton) {
                if(_buttleData.graphWrapper.currentSelectedNodeWrapper != m.nodeModel) {
                    _buttleData.graphWrapper.currentSelectedNodeWrapper = m.nodeModel
                    _buttleData.graphWrapper.zMax += 1
                    parent.z = _buttleData.graphWrapper.zMax
                }
                stateMoving.state = "moving"
                _buttleData.graphWrapper.updateConnectionsCoord()
            }
            // right button : we change the current param node
           else if (mouse.button == Qt.RightButton) {
                 _buttleData.graphWrapper.currentParamNodeWrapper = m.nodeModel;
            }


        }
        onReleased: {
            // left button : we end moving
            if (mouse.button == Qt.LeftButton) {
                _buttleData.graphWrapper.nodeMoved(m.nodeModel.name, parent.x, parent.y)
                stateMoving.state = "normal"
                _buttleData.graphWrapper.updateConnectionsCoord()
            }
        }
        // double click : we change the current viewer node
        onDoubleClicked: {
            _buttleData.graphWrapper.currentViewerNodeWrapper = m.nodeModel;
        }
    }
}

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
    width: _buttleData.graphWrapper.widthNode

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
        anchors.centerIn: parent
        radius: 10
        state: "normal"

        StateGroup {
            id: stateParamNode
             states: [
                 State {
                     name: "normal"
                     when: m.nodeModel != _buttleData.currentParamNodeWrapper
                     PropertyChanges {
                         target: nodeBorder;
                         height: parent.height;
                         width: parent.width;
                         color:  m.nodeModel.color;
                         opacity: 0.5;
                     }
                 },
                 State {
                     name: "currentParamNode"
                     when: m.nodeModel == _buttleData.currentParamNodeWrapper
                     PropertyChanges {
                         target: nodeBorder;
                         height: parent.height + 5;
                         width: parent.width + 5;
                         color:  "#00b2a1";
                         opacity: 1;
                     }
                 }
             ]
        }
    }

    Rectangle {
        id: nodeRectangle
        anchors.centerIn: parent
        height: parent.height - 8
        width: parent.width - 8
        color: "#bbbbbb"
        radius: 8
        Text {
            anchors.centerIn: parent
            text: m.nodeModel.nameUser
            font.pointSize: 10
            color: (m.nodeModel == _buttleData.currentSelectedNodeWrapper) ? "#00b2a1" : "black"
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

    Rectangle {
        id: deadMosquito
        width: 23
        height: 21
        x: node.width - 12
        y: -10
        state: "normal"
        color: "transparent"

        Image {
                id: deadMosquitoImage
                anchors.fill: parent
             }

        StateGroup {
            id: stateViewerNode
             states: [
                 State {
                     name: "normal"
                     when: m.nodeModel != _buttleData.currentViewerNodeWrapper
                     PropertyChanges {
                         target: deadMosquitoImage;
                         source: ""
                     }
                 },
                 State {
                     name: "currentViewerNode"
                     when: m.nodeModel == _buttleData.currentViewerNodeWrapper
                     PropertyChanges {
                         target: deadMosquitoImage;
                         source: "../img/mosquito_dead.png"
                     }
                 }
             ]
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
                if(_buttleData.currentSelectedNodeWrapper != m.nodeModel) {
                    _buttleData.currentSelectedNodeWrapper = m.nodeModel
                    _buttleData.graphWrapper.zMax += 1
                    parent.z = _buttleData.graphWrapper.zMax
                }
                stateMoving.state = "moving"
                _buttleData.graphWrapper.updateConnectionsCoord()
            }
            // right button : we change the current param node
           else if (mouse.button == Qt.RightButton) {
                 _buttleData.currentParamNodeWrapper = m.nodeModel;
            }
        }
        onReleased: {
            // left button : we end moving
            if (mouse.button == Qt.LeftButton) {
                _buttleData.nodeMoved(m.nodeModel.name, parent.x, parent.y)
                stateMoving.state = "normal"
            }
        }
        // double click : we change the current viewer node
        onDoubleClicked: {
            _buttleData.currentViewerNodeWrapper = m.nodeModel;
        }

    }

    onXChanged: {
        if (nodeMouseArea.drag.active) {
            node.nodeIsMoving()
        }
    }
    onYChanged: {
        if (nodeMouseArea.drag.active) {
            node.nodeIsMoving()
        }
    }

    function nodeIsMoving() {
        _buttleData.nodeIsMoving(m.nodeModel.name, node.x, node.y)
    }
}

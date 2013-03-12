import QtQuick 1.1
import QuickMamba 1.0

Rectangle {
    id: node

    QtObject {
        id: m
        property variant nodeModel: model.object
    }

    x: m.nodeModel.coord.x
    y: m.nodeModel.coord.y
    z: _buttleData.graphWrapper.zMax

    height: m.nodeModel.height
    width: nodeText.width + 20

    onWidthChanged: {
        model.object.setWidth(node.width)
    }

    property int inputSpacing : m.nodeModel.clipSpacing
    property int clipSize: m.nodeModel.clipSize
    property int nbInput: m.nodeModel.nbInput
    property int inputTopMargin: m.nodeModel.inputTopMargin
    property int outputTopMargin: m.nodeModel.outputTopMargin
    property int sideMargin: m.nodeModel.sideMargin

    signal drawSelection(int x, int y, int width, int height)

    color: "transparent"
    focus: true

    MouseArea {
        id: nodeMouseArea
        anchors.fill: parent
        drag.target: parent
        drag.axis: Drag.XandYAxis
        acceptedButtons: Qt.LeftButton | Qt.RightButton
        onPressed: {
            // left button : we change the current selected nodes & we start moving
            if (mouse.button == Qt.LeftButton) {
                _buttleData.graphWrapper.zMax += 1
                parent.z = _buttleData.graphWrapper.zMax
                stateMoving.state = "moving"
            }

            // right button : we change the current param node
           else if (mouse.button == Qt.RightButton) {
                // here display contextual menu
            }

            // take the focus
            node.forceActiveFocus()
        }
        onReleased: {
            // left button : we end moving
            if (mouse.button == Qt.LeftButton) {
                _buttleManager.nodeManager.nodeMoved(m.nodeModel.name, parent.x, parent.y)
                stateMoving.state = "normal"
            }
            if (mouse.button == Qt.LeftButton) {
                _buttleData.clearCurrentConnectionId()
                if(mouse.modifiers & Qt.ControlModifier){
                    _buttleData.appendToCurrentSelectedNodeWrappers(m.nodeModel)
                }
                else{
                    _buttleData.clearCurrentSelectedNodeNames()
                    _buttleData.appendToCurrentSelectedNodeWrappers(m.nodeModel)
                }
            }
        }
        // double click : we change the current param node
        onDoubleClicked: {
            _buttleData.currentParamNodeWrapper = m.nodeModel;
        }

    }

    DropArea {
        anchors.fill: parent
        onDrop: {
            if (hasText) {
                if(text=="mosquito_of_the_dead") {
                    _buttleData.currentViewerNodeWrapper = m.nodeModel;
                }
            }
        }
    }

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
                         target: nodeBorder
                         height: parent.height
                         width: parent.width
                         color:  m.nodeModel.color
                         opacity: 0.5
                     }
                 },
                 State {
                     name: "currentParamNode"
                     when: m.nodeModel == _buttleData.currentParamNodeWrapper
                     PropertyChanges {
                         target: nodeBorder;
                         height: parent.height
                         width: parent.width
                         color:  m.nodeModel.color
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
            id: nodeText
            anchors.centerIn: parent
            text: m.nodeModel.nameUser
            font.pointSize: 10
            property bool isSelected: _buttleData.nodeInCurrentSelectedNodeNames(m.nodeModel)
            
            Connections {
                target: _buttleData
                onCurrentSelectedNodeWrappersChanged: {
                    nodeText.isSelected = _buttleData.nodeInCurrentSelectedNodeNames(m.nodeModel)
                }
            }
            color: isSelected ? m.nodeModel.color : "black"
        }
    }
    //inputClips
    Column {
        id: nodeInputs
        anchors.left: parent.left
        anchors.leftMargin: -node.sideMargin
        anchors.top: parent.top
        anchors.topMargin: node.inputTopMargin
        spacing: node.inputSpacing
        Repeater {
            model: m.nodeModel.srcClips
            Clip {
                property string port : "input"
            }
        }
    }
    //outputClip
    Column {
        id: nodeOutputs
        anchors.right: parent.right
        anchors.rightMargin: -node.sideMargin
        anchors.top : parent.top
        anchors.topMargin: node.outputTopMargin
        spacing: node.inputSpacing
        // always only one outputClip
        Repeater {
            model: m.nodeModel.outputClips
            Clip {
                property string port : "output"
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
        _buttleManager.nodeManager.nodeIsMoving(m.nodeModel.name, node.x, node.y)
    }
}

import QtQuick 2.0
import QtQuick.Layouts 1.0

import QuickMamba 1.0


Rectangle {
    id: qml_nodeRoot

    property variant graphRoot
    property alias nodeWrapper: m.nodeWrapper

    Drag.active: nodeMouseArea.drag.active

    QtObject {
        id: m
        property variant nodeWrapper
        property variant nodeRoot: qml_nodeRoot

        property int inputSpacing: 10
        property int clipSize: 9
        property int nbInput: m.nodeWrapper.nbInput
        property int inputTopMargin: 10
        property int outputTopMargin: 10
        property int sideMargin: 10
    }
    objectName: "qmlNode_" + m.nodeWrapper.name

    x: m.nodeWrapper.coord.x
    y: m.nodeWrapper.coord.y
    z: _buttleData.graphWrapper.zMax

    height: 40
    width: 80

    signal drawSelection(int x, int y, int width, int height)

    color: "transparent"

    MouseArea {
        id: nodeMouseArea
        anchors.fill: parent
        drag.target: parent
        drag.axis: Drag.XandYAxis
        acceptedButtons: Qt.LeftButton | Qt.RightButton | Qt.MidButton
        onPressed: {
            // left button : we change the current selected nodes & we start moving
            if (mouse.button == Qt.LeftButton) {

                // we clear the list of selected connections
                _buttleData.clearCurrentConnectionId()

                // if the Control Key is not pressed, we clear the list of selected nodes
                if (!(mouse.modifiers & Qt.ControlModifier)) {
                    _buttleData.clearCurrentSelectedNodeNames()
                }

                // we add the node to the list of selected nodes (if it's not already selected)
                if(!_buttleData.nodeIsSelected(m.nodeWrapper)) {
                    _buttleData.appendToCurrentSelectedNodeWrappers(m.nodeWrapper)
                }

                _buttleData.graphWrapper.zMax += 1
                parent.z = _buttleData.graphWrapper.zMax
                stateMoving.state = "moving"
            }

            // right button : we change the current param node
           else if (mouse.button == Qt.RightButton) {
                // here display contextual menu
            }

            // take the focus
            m.nodeRoot.forceActiveFocus()
        }
        onReleased: {
            // left button : we end moving
            if (mouse.button == Qt.LeftButton) {
                _buttleManager.nodeManager.nodeMoved(m.nodeWrapper.name, parent.x, parent.y)
                stateMoving.state = "normal"
            }
             //middle button : assign the node to the viewer
            else if (mouse.button == Qt.MidButton){
                _buttleData.currentViewerNodeWrapper = m.nodeWrapper
                _buttleData.currentViewerFrame = 0
                // we assign the node to the viewer, at the frame 0
                _buttleData.assignNodeToViewerIndex(m.nodeWrapper, 0)
                _buttleEvent.emitViewerChangedSignal()
            }
            var dropStatus = parent.Drag.drop()
            if (dropStatus !== Qt.IgnoreAction)
                console.log("Accepted!")
        }

        // double click : we change the current param node
        onDoubleClicked: {
            _buttleData.currentParamNodeWrapper = m.nodeWrapper
        }

    }

    DropArea {
        anchors.fill: parent
        keys: "mosquitoMouseArea"

        onDropped: {
            _buttleData.currentViewerNodeWrapper = m.nodeWrapper
            _buttleData.currentViewerFrame = 0
            // we assign the node to the viewer, at the frame 0
            _buttleData.assignNodeToViewerIndex(m.nodeWrapper, 0)
            _buttleEvent.emitViewerChangedSignal()
        }
    }

    Rectangle {
        id: nodeBorder
        anchors.centerIn: parent
        radius: 10

        height: parent.height
        width: parent.width
        color:  m.nodeWrapper.color
        opacity: 0.5

        StateGroup {
            id: stateParamNode
             states: [
                 State {
                     name: "currentParamNode"
                     when: m.nodeWrapper == _buttleData.currentParamNodeWrapper
                     PropertyChanges {
                         target: nodeBorder
                         opacity: 1
                     }
                 }
             ]
        }
    }

    Rectangle {
        id: nodeRectangle
        anchors.centerIn: parent
        anchors.fill: parent
        anchors.margins: 4
        color: "#bbbbbb"
        radius: 8
        clip: true
        Text {
            id: nodeText
            anchors.verticalCenter: parent.verticalCenter
            x: 5
            text: m.nodeWrapper.nameUser
            font.pointSize: 10
            property bool isSelected: _buttleData.nodeIsSelected(m.nodeWrapper)
            
            // onTextChanged: {
            //     m.nodeWrapper.fitWidth(nodeText.width);
            //     // _buttleData.graphWrapper.updateConnectionsCoord(m.nodeWrapper);
            // }

            Connections {
                target: _buttleData
                onCurrentSelectedNodeWrappersChanged: {
                    nodeText.isSelected = _buttleData.nodeIsSelected(m.nodeWrapper)
                }
            }
            color: isSelected ? m.nodeWrapper.color : "black"
        }
    }
    RowLayout {
        id: inputClipsLayout
        anchors.fill: parent

        // inputClips
        Item {
            id: inputClipsItem
            height: parent.height
            Layout.minimumWidth: 20
            Layout.alignment: Qt.AlignVCenter | Qt.AlignLeft


            ListView {
                id: inputClipsContainer
                anchors.verticalCenter: parent.verticalCenter
                width: childrenRect.width
                height: childrenRect.height
                spacing: 5
                model: m.nodeWrapper.srcClips

                delegate: Component {
                    Clip {
                        id: in_clip
                        x_inGraph: qml_nodeRoot.x + inputClipsLayout.x + inputClipsItem.x + inputClipsContainer.x + x
                        y_inGraph: qml_nodeRoot.y + inputClipsLayout.y + inputClipsItem.y + inputClipsContainer.y + y

                        port: "input"
                        clipWrapper: model.object
                        graphRoot: m.nodeRoot.graphRoot
                        nodeRoot: m.nodeRoot
                        clipSize: m.clipSize
                        x:-10
                    }
                }
            }

        }
        Item {
            height: parent.height
            Layout.minimumWidth: 40
            Layout.fillWidth: true
        }

        // outputClip
        Item {
            id: outputClipContainer

            height: parent.height
            implicitWidth: childrenRect.width
            Layout.minimumWidth: childrenRect.width
            Layout.preferredWidth: childrenRect.width
            Layout.alignment: Qt.AlignVCenter | Qt.AlignRight
            // always only one output clip
            Clip {
                id: out_clip
                anchors.verticalCenter: parent.verticalCenter
                x_inGraph: qml_nodeRoot.x + outputClipContainer.x + x
                y_inGraph: qml_nodeRoot.y + outputClipContainer.y + y

                port: "output"
                clipWrapper: m.nodeWrapper.outputClip
                graphRoot: m.nodeRoot.graphRoot
                nodeRoot: m.nodeRoot
                clipSize: m.clipSize
                x:10
            }
        }
    }

    Rectangle {
        id: deadMosquito
        width: 23
        height: 21
        x: m.nodeRoot.width - 12
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
                     when: m.nodeWrapper != _buttleData.currentViewerNodeWrapper
                     PropertyChanges {
                         target: deadMosquitoImage;
                         source: ""
                     }
                 },
                 State {
                     name: "currentViewerNode"
                     when: m.nodeWrapper == _buttleData.currentViewerNodeWrapper
                     PropertyChanges {
                         target: deadMosquitoImage;
                         source: _buttleData.buttlePath + "/gui/img/mosquito/mosquito_dead.png"
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
                PropertyChanges { target: m.nodeRoot; x: m.nodeWrapper.coord.x; y: m.nodeWrapper.coord.y }
            },
            State {
                name: "moving"
                PropertyChanges { target: m.nodeRoot; x: m.nodeWrapper.coord.x ; y: m.nodeWrapper.coord.y }
            }
        ]
    }

    StateGroup {
        id: statePressed
        states: [
            State {
            name: "pressed"
            when: nodeMouseArea.pressed
            PropertyChanges { target: m.nodeRoot; opacity: .5 }
            }
        ]
    }

    onXChanged: {
        if (nodeMouseArea.drag.active) {
            m.nodeRoot.nodeIsMoving()
        }
    }
    onYChanged: {
        if (nodeMouseArea.drag.active) {
            m.nodeRoot.nodeIsMoving()
        }
    }

    function nodeIsMoving() {
        _buttleManager.nodeManager.nodeIsMoving(m.nodeWrapper.name, m.nodeRoot.x, m.nodeRoot.y)
    }
}

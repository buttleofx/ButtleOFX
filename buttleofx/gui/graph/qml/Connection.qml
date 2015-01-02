import QtQuick 2.0
import QuickMamba 1.0

Item {
    id: root
    property alias connectionWrapper: m.connectionWrapper

    property bool readOnly
    property bool miniatureState

    property int x1
    property int y1
    property int x2
    property int y2


    QtObject {
        id: m
        property variant connectionWrapper
    }

    CanvasConnection {
        id: connection

        x1: parent.x1
        y1: parent.y1
        x2: parent.x2
        y2: parent.y2

        visible: miniatureState ? false : true

        readOnly: root.readOnly
        miniatureState: root.miniatureState

        state: "normal"
        r: 0
        g: 178
        b: 161

        MouseArea {
            // Returns true if we click on the curve
            function intersectPath(mouseX, mouseY, margin){
                for (var x = mouseX - margin; x < mouseX + margin; x++) {
                    for (var y = mouseY - margin; y< mouseY + margin; y++) {
                        if (connection.getContext("2d").isPointInPath(x, y)) {
                            return true
                        }
                    }
                }
                return false
            }

            anchors.fill: parent
            hoverEnabled: true

            // Propagate the event to the connections below
            onPressed: mouse.accepted = intersectPath(mouseX, mouseY, 5)
            onClicked: {
                _buttleData.currentConnectionWrapper = m.connectionWrapper
                _buttleData.clearCurrentSelectedNodeNames()
            }

            // The accepted property of the MouseEvent parameter is ignored in this handler
            onPositionChanged: {
                mouse.accepted = intersectPath(mouseX, mouseY, 5)
            }
        }

        StateGroup {
            id: stateConnection
            states: [
                State {
                    name: "selectedConnection"
                    when: m.connectionWrapper == _buttleData.currentConnectionWrapper
                    PropertyChanges { target: connection; r: 187; g: 187; b: 187 }
                }
            ]
            // Need to re-paint the connection after each change of state
            onStateChanged: {
                connection.requestPaint()
            }
        }

        // Drop a node in the middle of the connection to insert it.
        DropArea {
            id: droparea1
            objectName: "DropArea"
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter

            width: 50 * zoomCoeff
            height: 50 * zoomCoeff
            Drag.keys: "node"

            onDropped: {
                var dragSrcClip = drop.source.nodeWrapper.srcClips.get(0)
                if (!_buttleManager.connectionManager.connectionExists(dragSrcClip)) {
                    // We assure that the node dropped is not part of the actual connection
                    if (drop.source.nodeWrapper !== undefined &&
                        drop.source.nodeWrapper.name != clipIn.nodeName &&
                        drop.source.nodeWrapper.name != clipOut.nodeName) {

                        drop.accept()
                        // Create two connections from one and delete the previous one
                        _buttleManager.connectionManager.dissociate(
                            clipOut, clipIn,
                            drop.source.nodeWrapper.getClip("Source"),
                            drop.source.nodeWrapper.getClip(drop.source.nodeWrapper.outputClip.name),
                            m.connectionWrapper)
                    }
                    dropIndicator.state = ""
                }
                // drop.source.nodeWrapper.xCoord = 0
                // m.nodeWrapper.coord.x
            }
            onEntered: {
                if (drag.source.nodeWrapper !== undefined && drag.source.nodeWrapper.name !== clipIn.nodeName &&
                    drag.source.nodeWrapper.name !== clipOut.nodeName) {
                    dropIndicator.state = "entereddrop"
                }
            }
            onExited: {
                dropIndicator.state = ""
            }

            Item {
                anchors.fill: parent
            }
        }

        Rectangle {
            id: dropIndicator
            anchors.centerIn: parent
            width: 12
            height: 12
            radius: 0.5 * width
            color: "#00b2a1"
            visible: false

            states: [
                State {
                    name: "entereddrop"

                    PropertyChanges {
                        target: dropIndicator
                        visible: true
                    }
                }
            ]
        }
    }
}

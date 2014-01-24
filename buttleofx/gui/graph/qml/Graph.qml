import QtQuick 2.0
import QuickMamba 1.0

Rectangle {
    id: qml_graphRoot


    Keys.onPressed: {

        // Graph toolbar
        if (event.key == Qt.Key_Delete) {
           _buttleManager.deleteSelection();
        }
    }


    QtObject {
        id: m
        property variant graphRoot: qml_graphRoot
    }

    signal clickCreationNode(string nodeType)
    signal drawSelection(int selectionX, int selectionY, int selectionWidth, int selectionHeight)

    property real zoomCoeff: 1
    property real zoomStep: 0.1
    property real nodeX
    property int offsetX: 0
    property int offsetY: 0
    property alias originX: graphContainer.x
    property alias originY: graphContainer.y

    property bool readOnly
    property bool miniatureState
    property real miniatureScale

    property var container: graphContainer

    /*
    ExternDropArea {
        anchors.fill: parent
        acceptDrop: true
        onDragEnter: {
            acceptDrop = hasUrls
        }
        onDrop: {
            console.log("Drop external files:", acceptDrop)
            if(acceptDrop) {
                _buttleManager.nodeManager.dropFile(firstUrl, pos.x - m.graphRoot.originX, pos.y - m.graphRoot.originY)
            }
        }
    }
    */

    // Drag&Drop from outside the app
    DropArea {
        id: graphDropArea
        anchors.fill: parent
        keys: ["text/uri-list"]

        onDropped: {
            if( ! drop.hasUrls )
            {
                drop.accepted = false
                return
            }

            for(var urlIndex in drop.urls)
            {
                _buttleManager.nodeManager.dropFile(drop.urls[urlIndex], drag.x - m.graphRoot.originX, drag.y - m.graphRoot.originY)
            }
            drop.accepted = true
        }
    }

    // Drag&Drop from Browser to Graph
    DropArea {
        anchors.fill: parent
        keys: "internFileDrag"

        onDropped: {
            _buttleManager.nodeManager.dropFile(drag.source.filePath, drag.x - m.graphRoot.originX, drag.y - m.graphRoot.originY)
            console.log("File dropped : ", drag.source.filePath)
        }
    }

    Rectangle {
        id: graphContainer
        x: 0
        y: 0
        width: parent.width * zoomCoeff
        height: parent.height * zoomCoeff
        color: "transparent"

        /*Item {
            id: repere
            property color repereColor: "red"
            property double size: 50 * zoomCoeff
            property double thickness: 2
            visible: miniatureState ? false : true
            Rectangle {
                id: axeX
                x: -repere.size - 0.5 * repere.thickness
                y: 0
                width: 2 * repere.size + repere.thickness
                height: 2
                color: repere.repereColor
            }
            Rectangle {
                id: axeY
                x: 0
                y: -repere.size - 0.5 * repere.thickness
                width: 2
                height: 2 * repere.size + repere.thickness
                color: repere.repereColor
            }
        }*/

        Item {
            id: nodes
            anchors.fill: parent
            z: 1

            Repeater {
                id: nodesRepeater
                model: _buttleData.graphWrapper.nodeWrappers
                Node {
                    id: node
                    nodeWrapper: model.object
                    graphRoot: m.graphRoot
                    width: nodeWidth * zoomCoeff
                    height: nodeWidth /2 * zoomCoeff
                    readOnly: qml_graphRoot.readOnly
                    miniatureScale: qml_graphRoot.miniatureScale
                    miniatureState: qml_graphRoot.miniatureState


                    StateGroup {
                        id: stateViewerNode
                         states: [
                             State {
                                 name: "miniatureState"
                                 when: miniatureState
                                 PropertyChanges {
                                     target: node
                                     width: node.nodeWidth * qml_graphRoot.miniatureScale
                                     height: node.nodeWidth /2 * qml_graphRoot.miniatureScale
                                 }
                             }
                         ]
                    }

                }
            }
        }

        Item {
            id: connections
            anchors.fill: parent
            // We set the z to 0 so the canvas is not over the node's clips
            z: 0
            Repeater {
                model : _buttleData.graphWrapper.connectionWrappers
                Connection {
                    id: connection
                    connectionWrapper: model.object
                    property variant nodeOut: _buttleData.graphWrapper.getNodeWrapper(connectionWrapper.out_clipNodeName)
                    property variant clipOut: nodeOut.getClip(connectionWrapper.out_clipName)

                    property variant nodeIn: _buttleData.graphWrapper.getNodeWrapper(connectionWrapper.in_clipNodeName)
                    property variant clipIn: nodeIn.getClip(connectionWrapper.in_clipName)

                    readOnly: qml_graphRoot.readOnly
                    miniatureState: qml_graphRoot.miniatureState
                    miniatureScale: qml_graphRoot.miniatureScale

                    x1: connection.miniatureState ? clipOut.xCoord * connection.miniatureScale : clipOut.xCoord
                    y1: connection.miniatureState ? clipOut.yCoord * connection.miniatureScale : clipOut.yCoord
                    x2: connection.miniatureState ? clipIn.xCoord * connection.miniatureScale : clipIn.xCoord
                    y2: connection.miniatureState ? clipIn.yCoord * connection.miniatureScale : clipIn.yCoord

                    visible: connectionWrapper.enabled ? true : false
                }
            }

            property bool tmpConnectionExists: false
            property string tmpClipName
            property int tmpConnectionX1
            property int tmpConnectionY1
            property int tmpConnectionX2
            property int tmpConnectionY2
            property real alpha: 1

            CanvasConnection {
                id: tmpCanvasConnection
                visible: connections.tmpConnectionExists ? true : false

                x1: connections.tmpConnectionX1
                y1: connections.tmpConnectionY1
                x2: connections.tmpConnectionX2
                y2: connections.tmpConnectionY2
                opacity: connections.alpha
            }
        }
    }
}

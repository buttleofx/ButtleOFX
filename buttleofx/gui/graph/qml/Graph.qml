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
    property real zoomStep: 0.05
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
                _buttleManager.nodeManager.dropFile(drop.urls[urlIndex], drag.x - m.graphRoot.originX + 10*urlIndex, drag.y - m.graphRoot.originY + 10*urlIndex)
            }
            drop.accepted = true
        }
    }

    // Drag&Drop from Browser to Graph
    DropArea {
        anchors.fill: parent
        keys: "internFileDrag"

        onDropped: {
            for(var urlIndex in drag.source.selectedFiles)
            {
                _buttleManager.nodeManager.dropFile(drag.source.selectedFiles[urlIndex], drag.x - m.graphRoot.originX + 10*urlIndex, drag.y - m.graphRoot.originY + 10*urlIndex)
            }
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
                }
            }

            property bool tmpConnectionExists: false
            property string tmpClipName
            property int tmpConnectionX1
            property int tmpConnectionY1
            property int tmpConnectionX2
            property int tmpConnectionY2

            CanvasConnection {
                id: tmpCanvasConnection
                visible: connections.tmpConnectionExists ? true : false

                x1: connections.tmpConnectionX1
                y1: connections.tmpConnectionY1
                x2: connections.tmpConnectionX2
                y2: connections.tmpConnectionY2
            }
        }
    }

    /*//Miniature de graph
    Rectangle{
        property real scaleFactor : 0.15
        property real marginTop : 150
        property real marginLeft : 70
        property alias miniOriginX: visuWindow.x
        property alias miniOriginY: visuWindow.y
        property int miniOffsetX: 0
        property int miniOffsetY: 0
        property real xOffset
        property real yOffset

        id: miniGraph
        width: (parent.width + marginLeft*2) * scaleFactor
        height: (parent.height + marginTop*2) * scaleFactor
        opacity: 0.8
        color: "#414141"
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        clip: true
        anchors.rightMargin: 10
        anchors.bottomMargin: 10

        Item {
            id: miniNodes
            anchors.fill: parent

            Repeater {
                id: miniNodesRepeater
                model: _buttleData.graphWrapper.nodeWrappers
                Rectangle {
                    width : 7
                    height : 7
                    radius: width * 0.5
                    //x: (((model.object.coord.x * graphContainer.width) / qml_graphRoot.width ) + ((qml_graphRoot.width * 0.5) - (graphContainer.width * 0.5)) + miniGraph.marginLeft) * miniGraph.scaleFactor
                    //y: (((model.object.coord.y * graphContainer.height) / qml_graphRoot.height ) + ((qml_graphRoot.height * 0.5) - (graphContainer.height * 0.5)) + miniGraph.marginTop) * miniGraph.scaleFactor
                    x: (model.object.coord.x + miniGraph.marginLeft) * miniGraph.scaleFactor
                    y: (model.object.coord.y + miniGraph.marginTop) * miniGraph.scaleFactor
                    color: "#00b2a1"
                    opacity: 1
                }
            }
            Rectangle {
                id: visuWindow
                property int previousW : qml_graphRoot.width * miniGraph.scaleFactor
                property int previousH : qml_graphRoot.height * miniGraph.scaleFactor
                border.color: "#00b2a1"
                border.width: 1
                opacity: 1
                color: "transparent"
                width: qml_graphRoot.width / zoomCoeff * miniGraph.scaleFactor
                height: qml_graphRoot.height / zoomCoeff * miniGraph.scaleFactor
                x: (miniGraph.marginLeft) * miniGraph.scaleFactor + ((previousW * 0.5) - (width * 0.5)) - offsetX * miniGraph.scaleFactor + miniGraph.miniOffsetX
                y: (miniGraph.marginTop) * miniGraph.scaleFactor + ((previousH * 0.5) - (height * 0.5)) - offsetY * miniGraph.scaleFactor + miniGraph.miniOffsetY
            }
        }

        MouseArea{
            anchors.fill: parent

            property int xStart
            property int yStart
            property int visuWindowXStart
            property int visuWindowYStart
            property bool moveMode: false

            hoverEnabled: true
            acceptedButtons: Qt.LeftButton
            onPressed: {
                xStart = mouse.x
                yStart = mouse.y
                visuWindowXStart = visuWindow.x
                visuWindowYStart = visuWindow.y
                moveMode = pressedButtons & Qt.LeftButton ? true : false
            }
            onReleased: {
                if(moveMode){
                    moveMode=false
                    miniGraph.xOffset = mouse.x - xStart
                    miniGraph.yOffset = mouse.y - yStart
                    parent.miniOffsetX += miniGraph.xOffset
                    parent.miniOffsetY += miniGraph.yOffset
                    graphContainer.x -= (miniGraph.xOffset/parent.scaleFactor)
                    graphContainer.y -= (miniGraph.yOffset/parent.scaleFactor)
                }
            }
        }
    }*/

}

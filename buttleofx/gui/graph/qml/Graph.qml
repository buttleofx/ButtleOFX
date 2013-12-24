import QtQuick 2.0
import QuickMamba 1.0

Item {
    id: qml_graphRoot

    QtObject {
        id: m
        property variant graphRoot: qml_graphRoot
    }

    property alias originX: graphContainer.x
    property alias originY: graphContainer.y

    signal clickCreationNode(string nodeType)
    signal drawSelection(int selectionX, int selectionY, int selectionWidth, int selectionHeight)

    // Selection area
    MouseArea {
        id: leftMouseArea
        property int xStart
        property int yStart
        property int graphContainer_xStart
        property int graphContainer_yStart

        property bool drawingSelection: false
        property bool selectMode: true

        anchors.fill: parent
        // hoverEnabled: true
        acceptedButtons: Qt.LeftButton
        onPressed: {
            xStart = mouse.x
            yStart = mouse.y
            graphContainer_xStart = graphContainer.x
            graphContainer_yStart = graphContainer.y

            rectangleSelection.x = mouse.x;
            rectangleSelection.y = mouse.y;
            rectangleSelection.width = 1;
            rectangleSelection.height = 1;
            selectMode = ! (mouse.modifiers & Qt.ControlModifier)
            if( selectMode ) {
                rectangleSelection.visible = true;
                drawingSelection = true;
            }
        }
        onReleased: {
            if( selectMode ) {
                rectangleSelection.visible = false;
                _buttleData.clearCurrentSelectedNodeNames();
                m.graphRoot.drawSelection(rectangleSelection.x - m.graphRoot.originX, rectangleSelection.y - m.graphRoot.originY, rectangleSelection.width, rectangleSelection.height)
            }
        }

        onPositionChanged: {
            if( mouse.x < xStart ) {
                rectangleSelection.x = mouse.x
                rectangleSelection.width = xStart - mouse.x;
            }
            else {
                rectangleSelection.width = mouse.x - xStart;
            }
            if( mouse.y < yStart ) {
                rectangleSelection.y = mouse.y
                rectangleSelection.height = yStart - mouse.y;
            }
            else {
                rectangleSelection.height = mouse.y - yStart;
            }

            if( ! selectMode ) {
                var xOffset = mouse.x - xStart
                var yOffset = mouse.y - yStart
                m.graphRoot.originX = graphContainer_xStart + xOffset
                m.graphRoot.originY = graphContainer_yStart + yOffset
            }
        }
    }
    onDrawSelection: {
        _buttleData.addNodeWrappersInRectangleSelection(selectionX, selectionY, selectionWidth, selectionHeight);
    }

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
    Rectangle {
        id: graphContainer
        x: 0
        y: 0
        width: parent.width
        height: parent.height

        color: "transparent"

        Item {
            id: repere
            property color repereColor: "red"
            property double size: 50
            property double thickness: 2
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
        }

        Item {
            id: nodes
            anchors.fill: parent
            z: 1

            Repeater {
                id: nodesRepeater
                model: _buttleData.graphWrapper.nodeWrappers
                Node {
                    nodeWrapper: model.object
                    graphRoot: m.graphRoot
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
                    connectionWrapper: model.object
                    property variant nodeOut: _buttleData.graphWrapper.getNodeWrapper(connectionWrapper.out_clipNodeName)
                    property variant clipOut: nodeOut.getClip(connectionWrapper.out_clipName)

                    property variant nodeIn: _buttleData.graphWrapper.getNodeWrapper(connectionWrapper.in_clipNodeName)
                    property variant clipIn: nodeIn.getClip(connectionWrapper.in_clipName)

                    x1: clipOut.xCoord
                    y1: clipOut.yCoord
                    x2: clipIn.xCoord
                    y2: clipIn.yCoord
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

    // Rectangle selection is placed here so it is drawn over the nodes
    Rectangle {
        id: rectangleSelection
        color: "white"
        border.color: "#00b2a1"
        opacity: 0.25
        visible: false
    }

    /*
    WheelArea {
        anchors.fill: parent
        property real nbSteps: 5
        onVerticalWheel: {
            if(scale.xScale > 0.3 ) {
                //scale.origin.x = middleMouseArea.mouseX
                //scale.origin.y = middleMouseArea.mouseY
                //console.log(connectnode.width)
                if(delta < 0 && scale.xScale - 0.2 > 0.3 && scale.yScale - 0.2 > 0.3 ) {
                    scale.xScale -= 0.1
                    scale.yScale -= 0.1
                }
                if(delta > 0) {
                    scale.xScale += 0.1
                    scale.yScale += 0.1
                }
            }
        }
    }
    */
}

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

    /*property real zoomCoeff: 1
    property real zoomStep: 0.05
    property real graphPreviousWidth: width
    property real graphPreviousHeight: height
    property int nodeInitialWidth: 80*/
    property int nodeWidth: 80

    property real zoomCoeff: 1
    property real zoomStep: 0.05
    property real graphPreviousWidth: width
    property real graphPreviousHeight: height
    property real nodeX
    property real mouseRatioX
    property real mouseRatioY
    property int offsetX: 0
    property int offsetY: 0

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
        property bool moveMode: false

        anchors.fill: parent
        hoverEnabled: true
        acceptedButtons: Qt.LeftButton | Qt.MiddleButton
        onPressed: {
            xStart = mouse.x
            yStart = mouse.y
            graphContainer_xStart = graphContainer.x
            graphContainer_yStart = graphContainer.y

            rectangleSelection.x = mouse.x;
            rectangleSelection.y = mouse.y;
            rectangleSelection.width = 1;
            rectangleSelection.height = 1;
            selectMode = leftMouseArea.pressedButtons & Qt.MiddleButton ? false : true
            moveMode = leftMouseArea.pressedButtons & Qt.MiddleButton ? true : false
            if( selectMode ) {
                rectangleSelection.visible = true;
                drawingSelection = true;
            }
        }
        onReleased: {
            if(moveMode){
                moveMode=false
                var xOffset = mouse.x - xStart
                var yOffset = mouse.y - yStart
                offsetX += xOffset
                offsetY += yOffset
            }
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

            if( moveMode ) {
                var xOffset = mouse.x - xStart
                var yOffset = mouse.y - yStart
                m.graphRoot.originX = graphContainer_xStart + xOffset
                m.graphRoot.originY = graphContainer_yStart + yOffset
            }
        }
        /*onWheel: {
            if(wheel.angleDelta.y > 0){
                zoomCoeff += zoomStep
            }else{
                if(zoomCoeff > zoomStep){ //inferior boundary
                    zoomCoeff -= zoomStep
                }
            }

            _buttleData.zoom(graphContainer.width, graphContainer.height, nodeWidth, zoomCoeff, graphPreviousWidth, graphPreviousHeight, mouseX, mouseY, m.graphRoot.originX, m.graphRoot.originY)
            graphPreviousWidth = zoomCoeff * graphContainer.width
            graphPreviousHeight = zoomCoeff * graphContainer.height
            nodeWidth = zoomCoeff * nodeInitialWidth
        }*/

        onWheel:{
            if(wheel.angleDelta.y > 0){
                zoomCoeff += zoomStep
            }else{
                zoomCoeff -= zoomStep
            }
            //mouseRatioX = (mouseX-offsetX)/graphContainer.width
            //mouseRatioY = (mouseY-offsetY)/graphContainer.height

            mouseRatioX = 0.5
            mouseRatioY = 0.5

            graphContainer.x = ((graphPreviousWidth * mouseRatioX) - (graphContainer.width * mouseRatioX)) + offsetX
            graphContainer.y = ((graphPreviousHeight * mouseRatioY) - (graphContainer.height * mouseRatioY )) + offsetY
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
        width: parent.width * zoomCoeff
        height: parent.height * zoomCoeff
        color: "transparent"

        Item {
            id: repere
            property color repereColor: "red"
            property double size: 50 * zoomCoeff
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
                    height: nodeWidth /2 * zoomCoeff
                    width: nodeWidth * zoomCoeff
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

    //Miniature de graph
    Rectangle{
        property real scaleFactor : 0.15
        property real marginTop : 150
        property real marginLeft : 70

        id: miniGraph
        width: (parent.width + marginLeft*2) * scaleFactor
        height: (parent.height + marginTop*2) * scaleFactor
        opacity: 0.5
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
                    //x: (((model.object.coord.x * graphContainer.width) / qml_graphRoot.graphPreviousWidth) + ((graphPreviousWidth * 0.5) - (graphContainer.width * 0.5)) + miniGraph.marginLeft) * miniGraph.scaleFactor
                    //y: (((model.object.coord.y * graphContainer.height) / qml_graphRoot.graphPreviousHeight) + ((graphPreviousHeight * 0.5) - (graphContainer.height * 0.5)) + miniGraph.marginTop) * miniGraph.scaleFactor
                    x: (model.object.coord.x + miniGraph.marginLeft) * miniGraph.scaleFactor
                    y: (model.object.coord.y + miniGraph.marginTop) * miniGraph.scaleFactor
                    color: "#00b2a1"
                    opacity: 1
                }
            }
            Rectangle {
                property int previousW : qml_graphRoot.width * miniGraph.scaleFactor
                property int previousH : qml_graphRoot.height * miniGraph.scaleFactor
                border.color: "#00b2a1"
                border.width: 1
                opacity: 1
                color: "transparent"
                width: qml_graphRoot.width / zoomCoeff * miniGraph.scaleFactor
                height: qml_graphRoot.height / zoomCoeff * miniGraph.scaleFactor
                x: (miniGraph.marginLeft) * miniGraph.scaleFactor + ((previousW * 0.5) - (width * 0.5))
                y: (miniGraph.marginTop) * miniGraph.scaleFactor + ((previousH * 0.5) - (height * 0.5))
            }
        }

        MouseArea{
            anchors.fill: parent
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
}

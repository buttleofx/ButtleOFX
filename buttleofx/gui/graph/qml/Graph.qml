import QtQuick 2.0
import QuickMamba 1.0

Item {
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
        hoverEnabled: true
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
                if(zoomCoeff > zoomStep){ //inferior boundary
                    zoomCoeff -= zoomStep
                }
            }
            //console.log("width" + graphContainer.width)
            //console.log("initial width" + graphPreviousWidth)
            //console.log("graphcontainer x" + graphContainer.x)
            graphContainer.x = (graphPreviousWidth * 0.5) - (graphContainer.width * 0.5)
            graphContainer.y = (graphPreviousHeight * 0.5) - (graphContainer.height * 0.5)
            //console.log("container xstart" + graphContainer_xStart)
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
        border.color : "green"
        border.width : 5
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

    // Rectangle selection is placed here so it is drawn over the nodes
    Rectangle {
        id: rectangleSelection
        color: "white"
        border.color: "#00b2a1"
        opacity: 0.25
        visible: false
    }
}

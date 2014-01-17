import QtQuick 2.0
import QtQuick.Layouts 1.0

Item {
    id: graphEditor

    ColumnLayout {
        anchors.fill: parent
        spacing: 2

        Tools {
            id: tools
            implicitWidth : parent.width
            Layout.minimumHeight: 40
            Layout.preferredHeight: 40
            implicitHeight: 40
            menuComponent: null

            onClickCreationNode: {
                // console.log("Node created clicking from Tools")
                _buttleManager.nodeManager.creationNode(nodeType, -graph.originX + 20, -graph.originY + 20)
            }
        }
        Item {
            implicitWidth: parent.width
            Layout.minimumHeight: 100
            implicitHeight: 300
            Layout.fillHeight: true

            Graph{
                id: graph
                implicitWidth: parent.width
                Layout.minimumHeight: 100
                implicitHeight: 300
                Layout.fillHeight: true
                clip: true
                color: "transparent"
                readOnly: false
                miniatureState: false
                onClickCreationNode: {
                    // console.log("Node created clicking from Graph")
                    _buttleManager.nodeManager.creationNode(nodeType, -graph.originX + graph.mouseX, -graph.originY + graph.mouseY)
                }

                MouseArea {
                    id: leftMouseArea
                    property int xStart
                    property int yStart
                    property int graphContainer_xStart
                    property int graphContainer_yStart

                    property bool drawingSelection: false
                    property bool selectMode: true
                    property bool moveMode: false

                    z: -1
                    anchors.fill: parent
                    hoverEnabled: true
                    acceptedButtons: Qt.LeftButton | Qt.MiddleButton
                    onPressed: {
                        xStart = mouse.x
                        yStart = mouse.y
                        graphContainer_xStart = parent.container.x
                        graphContainer_yStart = parent.container.y

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
                            graph.offsetX += xOffset
                            graph.offsetY += yOffset
                        }
                        if( selectMode ) {
                            rectangleSelection.visible = false;
                            _buttleData.clearCurrentSelectedNodeNames();
                            graph.drawSelection(rectangleSelection.x - graph.originX, rectangleSelection.y - graph.originY, rectangleSelection.width, rectangleSelection.height)
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
                            graph.originX = graphContainer_xStart + xOffset
                            graph.originY = graphContainer_yStart + yOffset
                        }
                    }

                    onWheel:{
                        if(wheel.angleDelta.y > 0){
                            graph.zoomCoeff += graph.zoomStep
                        }else{
                            graph.zoomCoeff -= graph.zoomStep
                        }

                        var mouseRatioX = 0.5
                        var mouseRatioY = 0.5
                        parent.container.x = ((graph.width * mouseRatioX) - (parent.container.width * mouseRatioX)) + graph.offsetX - miniGraph.miniOffsetX / miniGraph.scaleFactor
                        parent.container.y = ((graph.height * mouseRatioY) - (parent.container.height * mouseRatioY )) + graph.offsetY - miniGraph.miniOffsetY / miniGraph.scaleFactor
                    }
                }
                onDrawSelection: {
                    _buttleData.addNodeWrappersInRectangleSelection(selectionX, selectionY, selectionWidth, selectionHeight);
                }

                Rectangle {
                    id: rectangleSelection
                    color: "white"
                    border.color: "#00b2a1"
                    opacity: 0.25
                    visible: false
                }
            }

            //The miniature of the graph
            Rectangle{
                id: miniGraph
                property real scaleFactor: 0.15
                property real marginTop: 300
                property real marginLeft: 0
                property real xOffset
                property real yOffset
                property int miniOffsetX: 0
                property int miniOffsetY: 0
                property alias originX : tmpVisuWindow.x
                property alias originY : tmpVisuWindow.y
                property int previousW : graph.width * scaleFactor
                property int previousH : graph.height * scaleFactor
                property bool tmpMode : false

                anchors.top: graph.top
                anchors.right: graph.right
                anchors.margins: 10
                width: graph.width * scaleFactor
                height: (graph.height + marginTop) * scaleFactor
                color: "#434343"
                opacity: 0.7

                MouseArea{
                    anchors.fill: parent
                    width: miniGraph.width
                    height: miniGraph.height
                    id: miniatureArea
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
                        visuWindowXStart = tmpVisuWindow.x
                        visuWindowYStart = tmpVisuWindow.y
                        moveMode = pressedButtons & Qt.LeftButton ? true : false
                    }
                    onReleased: {
                        if(moveMode){
                            moveMode = false
                            miniGraph.tmpMode = false
                            miniGraph.xOffset = mouse.x - xStart
                            miniGraph.yOffset = mouse.y - yStart
                            miniGraph.miniOffsetX += miniGraph.xOffset
                            miniGraph.miniOffsetY += miniGraph.yOffset
                            graph.container.x -= (miniGraph.xOffset/miniGraph.scaleFactor)
                            graph.container.y -= (miniGraph.yOffset/miniGraph.scaleFactor)

                            //to map the tmpVisuWindow (zoom)
                            miniGraph.originX = visuWindow.x
                            miniGraph.originY = visuWindow.y
                            tmpVisuWindow.width = visuWindow.width
                            tmpVisuWindow.height = visuWindow.height
                        }
                    }
                    onPositionChanged: {
                        if(moveMode){
                            miniGraph.tmpMode = true
                            var xOffset = mouse.x - xStart
                            var yOffset = mouse.y - yStart
                            miniGraph.originX = visuWindowXStart + xOffset
                            miniGraph.originY = visuWindowYStart + yOffset
                        }else{ //to map the tmpVisuWindow (zoom)
                            miniGraph.originX = visuWindow.x
                            miniGraph.originY = visuWindow.y
                            tmpVisuWindow.width = visuWindow.width
                            tmpVisuWindow.height = visuWindow.height
                        }
                    }
                }

                Graph {
                    id: graphMiniature
                    readOnly: true
                    miniatureState: true
                    miniatureScale: parent.scaleFactor
                    width: parent.width
                    height: parent.height - (parent.marginTop * parent.scaleFactor)
                    color: "transparent"
                    y: (parent.marginTop * 0.5) * parent.scaleFactor
                    opacity: 1
                }

                Rectangle {
                    id: visuWindow
                    border.color: height > miniGraph.height ? "transparent" : "white"
                    border.width: 1
                    color: "transparent"
                    width: graph.width / graph.zoomCoeff * miniGraph.scaleFactor
                    height: graph.height / graph.zoomCoeff * miniGraph.scaleFactor
                    visible: !miniGraph.tmpMode
                    x: (miniGraph.marginLeft * 0.5) * miniGraph.scaleFactor + ((miniGraph.previousW * 0.5) - (width * 0.5)) - graph.offsetX * miniGraph.scaleFactor + miniGraph.miniOffsetX
                    y: (miniGraph.marginTop * 0.5) * miniGraph.scaleFactor + ((miniGraph.previousH * 0.5) - (height * 0.5)) - graph.offsetY * miniGraph.scaleFactor + miniGraph.miniOffsetY
                }

                Rectangle {
                    id: tmpVisuWindow
                    border.color: "#00b2a1"
                    border.width: 1
                    color: "transparent"
                    visible: miniGraph.tmpMode
                    width: graph.width / graph.zoomCoeff * miniGraph.scaleFactor
                    height: graph.height / graph.zoomCoeff * miniGraph.scaleFactor
                    x: (miniGraph.marginLeft * 0.5) * miniGraph.scaleFactor + ((miniGraph.previousW * 0.5) - (width * 0.5)) - graph.offsetX * miniGraph.scaleFactor + miniGraph.miniOffsetX
                    y: (miniGraph.marginTop * 0.5) * miniGraph.scaleFactor + ((miniGraph.previousH * 0.5) - (height * 0.5)) - graph.offsetY * miniGraph.scaleFactor + miniGraph.miniOffsetY
                }
            }
        }

    }
}

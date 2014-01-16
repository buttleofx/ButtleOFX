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

                        parent.container.x = ((graph.width * mouseRatioX) - (parent.container.width * mouseRatioX)) + graph.offsetX
                        parent.container.y = ((graph.height * mouseRatioY) - (parent.container.height * mouseRatioY )) + graph.offsetY
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
                property real scaleFactor: 0.15
                property real margins: 300
                anchors.top: graph.top
                anchors.right: graph.right
                anchors.margins: 10
                width: graph.width * scaleFactor
                height: (graph.height + margins) * scaleFactor
                color: "#434343"
                opacity: 0.7

                Graph {
                    id: graphMiniature
                    readOnly: true
                    miniatureState: true
                    miniatureScale: parent.scaleFactor
                    width: parent.width
                    height: parent.height - (parent.margins * parent.scaleFactor)
                    color: "transparent"
                    y: (parent.margins * 0.5) * parent.scaleFactor
                    opacity: 1
                }

                Rectangle {
                    id: visuWindow
                    border.color: "white"
                    border.width: 1
                    color: "transparent"
                    anchors.fill: graphMiniature
                }
            }
        }

    }
}

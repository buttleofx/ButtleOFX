import QtQuick 2.0
import QtQuick.Layouts 1.0

import "../../../gui"

Item {
    id: graphEditor

    signal buttonCloseClicked(bool clicked)  
    signal buttonFullscreenClicked(bool clicked)

    Tab {
        id: tabBar
        name: "Graph"
        onCloseClicked: graphEditor.buttonCloseClicked(true)
        onFullscreenClicked: graphEditor.buttonFullscreenClicked(true)
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.topMargin: tabBar.height
        spacing: 2

        Tools {
            id: tools
            //y: tabBar.height
            implicitWidth : parent.width
            Layout.minimumHeight: 40
            Layout.preferredHeight: 40
            implicitHeight: 40
            menuComponent: null

            onClickCreationNode: {
                // console.log("Node created clicking from Tools")
                _buttleData.currentGraphIsGraph()
                _buttleData.currentGraphWrapper = _buttleData.graphWrapper
                // if before the viewer was showing an image from the brower, we change the currentView
                if (_buttleData.currentViewerIndex > 9){
                    _buttleData.currentViewerIndex = player.lastView
                    if (player.lastNodeWrapper != undefined)
                        _buttleData.currentViewerNodeWrapper = player.lastNodeWrapper
                    player.changeViewer(player.lastView)                    
                }
                _buttleManager.nodeManager.creationNode("_buttleData.graph", nodeType, -graph.originX + 20, -graph.originY + 20)
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
                height: parent.height
                Layout.fillHeight: true
                clip: true
                color: "transparent"
                readOnly: false
                miniatureState: false
                onClickCreationNode: {
                    // console.log("Node created clicking from Graph")
                    _buttleData.currentGraphIsGraph()
                    _buttleData.currentGraphWrapper = _buttleData.graphWrapper
                    // if before the viewer was showing an image from the brower, we change the currentView
                    if (_buttleData.currentViewerIndex > 9){
                        _buttleData.currentViewerIndex = player.lastView
                        if (player.lastNodeWrapper != undefined)
                            _buttleData.currentViewerNodeWrapper = player.lastNodeWrapper
                        player.changeViewer(player.lastView)
                    }
                    _buttleManager.nodeManager.creationNode("_buttleData.graph", nodeType, -graph.originX + graph.mouseX, -graph.originY + graph.mouseY)
                }

                MouseArea {
                    id: leftMouseArea
                    property real xStart
                    property real yStart
                    property real graphContainer_xStart
                    property real graphContainer_yStart

                    property bool drawingSelection: false
                    property bool selectMode: true
                    property bool moveMode: false

                    z: -1
                    anchors.fill: parent
                    hoverEnabled: true
                    acceptedButtons: Qt.LeftButton | Qt.MiddleButton
                    onPressed: {
                        pluginVisible=false
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
                            if(graph.zoomCoeff - graph.zoomStep >= 0)
                                graph.zoomCoeff -= graph.zoomStep
                        }

                        var mouseRatioX = 0.5
                        var mouseRatioY = 0.5
                        parent.container.x = ((graph.width * mouseRatioX) - (parent.container.width * mouseRatioX)) + graph.offsetX - miniGraph.miniOffsetX / miniGraph.scaleFactor *graph.zoomCoeff
                        parent.container.y = ((graph.height * mouseRatioY) - (parent.container.height * mouseRatioY )) + graph.offsetY - miniGraph.miniOffsetY / miniGraph.scaleFactor *graph.zoomCoeff
                    }
                }
                onDrawSelection: {
                    _buttleData.addNodeWrappersInRectangleSelection(selectionX / container.width * graph.width, selectionY / container.width * graph.width, selectionWidth / graph.zoomCoeff, selectionHeight / graph.zoomCoeff);
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
                property real scaleFactor: 0.05
                property real marginTop: 1600
                property real marginLeft: 2000
                property real xOffset
                property real yOffset
                property real miniOffsetX: 0
                property real miniOffsetY: 0
                property alias originX : tmpVisuWindow.x
                property alias originY : tmpVisuWindow.y
                property real previousW : graph.width * scaleFactor
                property real previousH : graph.height * scaleFactor
                property bool tmpMode : false

                anchors.top: graph.top
                anchors.right: graph.right
                anchors.margins: 10
                width: (graph.width + marginLeft) * scaleFactor
                height: (graph.height + marginTop) * scaleFactor
                color: "#434343"
                opacity: 0.7
                clip: true

                MouseArea{
                    anchors.fill: parent
                    width: miniGraph.width
                    height: miniGraph.height
                    id: miniatureArea
                    property real xStart
                    property real yStart
                    property real visuWindowXStart
                    property real visuWindowYStart
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
                            if(mouse.x>0 && mouse.x < miniGraph.width){
                                miniGraph.xOffset = mouse.x - xStart
                            }else if(mouse.x > miniGraph.width){
                                miniGraph.xOffset = miniGraph.width - xStart
                            }else{
                                miniGraph.xOffset = -xStart
                            }

                            if(mouse.y > 0 && mouse.y < miniGraph.height){
                                miniGraph.yOffset = mouse.y - yStart
                            }else if (mouse.y > miniGraph.height){
                                miniGraph.yOffset = miniGraph.height - yStart
                            }else{
                                miniGraph.yOffset = -yStart
                            }

                            miniGraph.miniOffsetX += miniGraph.xOffset
                            miniGraph.miniOffsetY += miniGraph.yOffset
                            graph.container.x -= (miniGraph.xOffset/miniGraph.scaleFactor*graph.zoomCoeff)
                            graph.container.y -= (miniGraph.yOffset/miniGraph.scaleFactor*graph.zoomCoeff)

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
                            if((mouse.x > 0 && mouse.x < miniGraph.width) && (mouse.y > 0 && mouse.y < miniGraph.height)){
                                var xOffset = mouse.x - xStart
                                var yOffset = mouse.y - yStart
                                miniGraph.originX = visuWindowXStart + xOffset
                                miniGraph.originY = visuWindowYStart + yOffset
                            }
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
                    width: parent.width - (parent.marginLeft * parent.scaleFactor)
                    height: parent.height - (parent.marginTop * parent.scaleFactor)
                    color: "transparent"
                    x: (parent.marginLeft * 0.5) * parent.scaleFactor
                    y: (parent.marginTop * 0.5) * parent.scaleFactor
                    opacity: 1
                }

                Rectangle {
                    id: visuWindow
                    border.color: "white"
                    border.width: 1
                    color: "transparent"
                    width: graph.width / graph.zoomCoeff * miniGraph.scaleFactor
                    height: graph.height / graph.zoomCoeff * miniGraph.scaleFactor
                    visible: !miniGraph.tmpMode
                    x: (miniGraph.marginLeft * 0.5) * miniGraph.scaleFactor + ((miniGraph.previousW * 0.5) - (width * 0.5)) - graph.offsetX * miniGraph.scaleFactor / graph.zoomCoeff + miniGraph.miniOffsetX
                    y: (miniGraph.marginTop * 0.5) * miniGraph.scaleFactor + ((miniGraph.previousH * 0.5) - (height * 0.5)) - graph.offsetY * miniGraph.scaleFactor / graph.zoomCoeff+ miniGraph.miniOffsetY
                }

                Rectangle {
                    id: tmpVisuWindow
                    border.color: "#00b2a1"
                    border.width: 1
                    color: "transparent"
                    visible: miniGraph.tmpMode
                    width: graph.width / graph.zoomCoeff * miniGraph.scaleFactor
                    height: graph.height / graph.zoomCoeff * miniGraph.scaleFactor+15
                    x: (miniGraph.marginLeft * 0.5) * miniGraph.scaleFactor + ((miniGraph.previousW * 0.5) - (width * 0.5)) - graph.offsetX * miniGraph.scaleFactor / graph.zoomCoeff+ miniGraph.miniOffsetX
                    y: (miniGraph.marginTop * 0.5) * miniGraph.scaleFactor + ((miniGraph.previousH * 0.5) - (height * 0.5)) - graph.offsetY * miniGraph.scaleFactor / graph.zoomCoeff+ miniGraph.miniOffsetY
                }
            }
        }

    }
}

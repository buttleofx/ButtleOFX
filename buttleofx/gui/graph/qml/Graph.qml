import QtQuick 1.1
import QuickMamba 1.0
import ConnectionLineItem 1.0
import Canvas 1.0

Rectangle {
    id:graphArea
    y: 30
    z: 0
    width: 850
    height: 350 - y

    property alias originX: connectnode.x
    property alias originY: connectnode.y

    //property alias mouseX: mouseArea.mouseX
    //property alias mouseY: mouseArea.mouseY

    signal clickCreationNode(string nodeType)
    color: "#191919"
//    gradient: Gradient {
//        GradientStop { position: 0.0; color: "#111111" }
//        GradientStop { position: 0.015; color: "#212121" }
//    }

    Rectangle {
        id: connectnode
        Item {
            id: nodes
            width: graphArea.width
            height: graphArea.height
            z: 1
            Repeater {
                model : _buttleData.graphWrapper.nodeWrappers
                Node {
                    Component.onDestruction: {
                        nodes.forceActiveFocus()
                    }
                }
            }
        }

        Item{
            id: connections
            width: graphArea.width
            height: graphArea.height
            // We set the z to 0 so the canvas is not over the node's clips
            z: 0
            Repeater {
                model : _buttleData.graphWrapper.connectionWrappers
//                ConnectionLine {
//                    x1: model.object.clipOutPosX
//                    y1: model.object.clipOutPosY
//                    x2: model.object.clipInPosX
//                    y2: model.object.clipInPosY
//                }
                Canvas {
                    id: connection
                    property int canvasMargin: 20
                    property int inPath: 0
                    width: Math.abs(model.object.clipOutPosX - model.object.clipInPosX) + 2*canvasMargin
                    height: Math.abs(model.object.clipOutPosY - model.object.clipInPosY) + 2*canvasMargin

                    x: Math.min(model.object.clipOutPosX, model.object.clipInPosX) - canvasMargin
                    y: Math.min(model.object.clipOutPosY, model.object.clipInPosY) - canvasMargin

                    color: "transparent"
                    onPaint: {
                        var ctx = getContext();
                        var cHeight = height;
                        var cWidth = width;
                        var startX = 0
                        var startY = 0
                        var endX = 0
                        var endY = 0
                        var controlPointXOffset = 40;
                        ctx.strokeStyle = "rgb(0,150,70)";
                        ctx.lineWidth = 2;

                        ctx.beginPath()

                        if(model.object.clipOutPosX <= model.object.clipInPosX
                        && model.object.clipOutPosY <= model.object.clipInPosY){
                            startX = canvasMargin
                            startY = canvasMargin
                            endX = width - canvasMargin
                            endY = height - canvasMargin
                        }
                        if(model.object.clipOutPosX <= model.object.clipInPosX
                        && model.object.clipOutPosY > model.object.clipInPosY){
                            startX = canvasMargin
                            startY = height - canvasMargin
                            endX = width - canvasMargin
                            endY = canvasMargin
                        }
                        if(model.object.clipOutPosX > model.object.clipInPosX
                        && model.object.clipOutPosY <= model.object.clipInPosY){
                            startX = width - canvasMargin
                            startY = canvasMargin
                            endX = canvasMargin
                            endY = height - canvasMargin
                        }
                        if(model.object.clipOutPosX > model.object.clipInPosX
                        && model.object.clipOutPosY > model.object.clipInPosY){
                            startX = width - canvasMargin
                            startY = height - canvasMargin
                            endX = canvasMargin
                            endY = canvasMargin
                        }

                        ctx.moveTo(startX , startY)
                        ctx.bezierCurveTo(startX + controlPointXOffset, startY, endX - controlPointXOffset, endY, endX, endY)
                        ctx.stroke()
                        ctx.closePath()
                    }

                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            for(var x = mouseX - 5; x< mouseX + 5; x++){
                                for(var y = mouseY - 5; y< mouseY + 5; y++){
                                    if(connection.getContext().isPointInPath(x, y)){
                                        inPath = 1
                                        return true;
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        transform: Scale { id: scale; origin.x: graphArea.width/2; origin.y: graphArea.height/2; xScale: 1; yScale: 1}
    }
    


    MouseArea{
        id: middleMouseArea
        anchors.fill: parent
        acceptedButtons: Qt.MiddleButton 
        hoverEnabled: true
        drag.target: connectnode
        drag.axis: Drag.XandYAxis
    }

    WheelArea {
        anchors.fill: parent
        property real nbSteps: 5
        onVerticalWheel: {
            if(scale.xScale > 0.3 ) {
                //scale.origin.x = middleMouseArea.mouseX
                //scale.origin.y = middleMouseArea.mouseY
                console.log(connectnode.width)
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

    /*  // NODE CREATION WITH RIGHT CLICK
        MouseArea{
        id: mouseArea
        anchors.fill: parent
        acceptedButtons: Qt.RightButton
        onClicked: {
             if (mouse.button == Qt.RightButton)
             listmodel.x = mouseX
             listmodel.y = mouseY - 30
             listmodel.clickFrom = graphArea
             listmodel.menuState = (listmodel.menuState == "hidden") ? "shown" : "hidden"
        }
    } */

    DropArea {
        anchors.fill: parent
        onDrop: {
            if( hasUrls )
            {
                _buttleData.dropReaderNode(firstUrl, pos.x, pos.y)
            }
        }
    }
    
}

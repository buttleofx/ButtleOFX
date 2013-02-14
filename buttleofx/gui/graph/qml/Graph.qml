import QtQuick 1.1
import QuickMamba 1.0
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
    color: "#212121"

    MouseArea{
        id: leftMouseArea
        anchors.fill: parent
        acceptedButtons: Qt.LeftButton
        onClicked: {
            if (tools.menuComponent) {
                tools.menuComponent.destroy();
            }
        }
    }

    MouseArea{
        id: middleMouseArea
        anchors.fill: parent
        acceptedButtons: Qt.MiddleButton
        hoverEnabled: true
        drag.target: connectnode
        drag.axis: Drag.XandYAxis
    }

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

        Item {
            id: connections
            width: graphArea.width
            height: graphArea.height
            // We set the z to 0 so the canvas is not over the node's clips
            z: 0
            Repeater {
                model : _buttleData.graphWrapper.connectionWrappers
                Canvas {
                    id: connection

                    QtObject {
                        id: m
                        property variant connectionModel: model.object
                    }

                    property int canvasMargin: 20
                    property int inPath: 0
                    property int r: 0
                    property int g: 178
                    property int b: 161

                    width: Math.abs(model.object.clipOutPosX - model.object.clipInPosX) + 2*canvasMargin
                    height: Math.abs(model.object.clipOutPosY - model.object.clipInPosY) + 2*canvasMargin
                    x: Math.min(model.object.clipOutPosX, model.object.clipInPosX) - canvasMargin
                    y: Math.min(model.object.clipOutPosY, model.object.clipInPosY) - canvasMargin
                    color: "transparent"
                    state: m.connectionModel == _buttleData.currentConnectionWrapper ? "selectedConnection" :"notSelectedConnection"

                    StateGroup{
                        id: stateConnection
                        states: [
                            State {
                                name: "selectedConnection"
                                when: m.connectionModel == _buttleData.currentConnectionWrapper
                                PropertyChanges { target: connection; r: 255; g: 255; b: 255 }
                            },
                            State {
                                name: "notSelectedConnection"
                                when: m.connectionModel != _buttleData.currentConnectionWrapper
                                PropertyChanges { target: connection; r: 0; g: 178; b: 161 }
                            }
                        ]
                    }

                    onPaint: {
                        var ctx = getContext();
                        var cHeight = height;
                        var cWidth = width;
                        var startX = 0
                        var startY = 0
                        var endX = 0
                        var endY = 0
                        var controlPointXOffset = 40;
                        ctx.strokeStyle = "rgb("+r+", "+g+", "+b+")";
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

                    function intersectPath(mouseX, mouseY, margin){
                        for(var x = mouseX - margin; x< mouseX + margin; x++){
                            for(var y = mouseY - margin; y< mouseY + margin; y++){
                                if(connection.getContext().isPointInPath(x, y)){
                                    return true;
                                }
                            }
                        }
                        return false;
                    }

                    MouseArea {
                        anchors.fill: parent
                        hoverEnabled: true

                        //Propagate the event to the connections below
                        onPressed: mouse.accepted = intersectPath(mouseX, mouseY, 5)
                        onClicked: {
                            _buttleData.currentConnectionWrapper = m.connectionModel
                            connection.requestPaint()
                        }
                        // The accepted property of the MouseEvent parameter is ignored in this handler.
                        //onPositionChanged: {
                        //    mouse.accepted = intersectPath(mouseX, mouseY, 5)
                        //    console.log("Mouse accepted : " + mouse.accepted)
                        //}
                    }
                }
            }
        }

        transform: Scale { id: scale; origin.x: graphArea.width/2; origin.y: graphArea.height/2; xScale: 1; yScale: 1}
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
        {
        id: rightMouseArea
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

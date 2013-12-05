import QtQuick 2.0
import QuickMamba 1.0

Rectangle {
    id:graphArea
    y: 30
    z: 0
    width: 850
    height: 350 - y

    property alias originX: connectnode.x
    property alias originY: connectnode.y

    property alias mouseX: rightMouseArea.mouseX
    property alias mouseY: rightMouseArea.mouseY

    signal clickCreationNode(string nodeType)
    signal drawSelection(int selectionX, int selectionY, int selectionWidth, int selectionHeight)

    color: "#212121"

    // Selection area

    MouseArea {
        id: leftMouseArea
        property int xStart
        property int yStart
        property bool drawingSelection : false

        anchors.fill: parent
        hoverEnabled: true
        acceptedButtons: Qt.LeftButton
        onClicked: {
            if (tools.menuComponent) {
                tools.menuComponent.destroy();
            }
        }
        onPressed: {
            xStart = mouse.x;
            yStart = mouse.y;
            rectangleSelection.x = mouse.x;
            rectangleSelection.y = mouse.y;
            rectangleSelection.width = 1;
            rectangleSelection.height = 1;
            rectangleSelection.visible = true;
            drawingSelection: true;
        }
        onReleased: {
            rectangleSelection.visible = false;
            _buttleData.clearCurrentSelectedNodeNames();
            graphArea.drawSelection(rectangleSelection.x - graphArea.originX, rectangleSelection.y - graphArea.originY, rectangleSelection.width, rectangleSelection.height)
        }

        onPositionChanged: {
            if(mouse.x < xStart){
                rectangleSelection.x = mouse.x
                rectangleSelection.width = xStart - mouse.x;
            }
            else {
                rectangleSelection.width = mouse.x - xStart;
            }
            if(mouse.y < yStart){
                rectangleSelection.y = mouse.y
                rectangleSelection.height = yStart - mouse.y;
            }
            else {
                rectangleSelection.height = mouse.y - yStart;
            }
        }
    }
    onDrawSelection: {
        _buttleData.addNodeWrappersInRectangleSelection(selectionX, selectionY, selectionWidth, selectionHeight);
    }

    MouseArea{
        id: middleMouseArea
        anchors.fill: parent
        acceptedButtons: Qt.MiddleButton
        hoverEnabled: true
        drag.target: connectnode
        drag.axis: Drag.XandYAxis
    }
    DropArea {
        anchors.fill: parent
        onEntered: {
          console.log("onEntered")
        }
        onDropped: {
          console.log("onDropped")
        }
    }
    ExternDropArea {
        anchors.fill: parent
        acceptDrop: false
        onDragEnter: {
            acceptDrop = hasUrls;

            // tmpConnection update
            if(hasText && text.substring(0, 5) == "clip/") {
                if (connections.tmpClipName == "Output") {
                    connections.tmpConnectionX2 =  pos.x - graphArea.originX
                    connections.tmpConnectionY2 =  pos.y - graphArea.originY
                }
                else {
                    connections.tmpConnectionX1 =  pos.x - graphArea.originX
                    connections.tmpConnectionY1 =  pos.y - graphArea.originY
                }
            }
        }

        onDrop: {
            if(acceptDrop) {
                _buttleManager.nodeManager.dropFile(firstUrl, pos.x - graphArea.originX, pos.y - graphArea.originY)
            }
        }

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
                Connection {
                    connectionModel: model.object
                    x1: model.object.clipOutPosX
                    y1: model.object.clipOutPosY
                    x2: model.object.clipInPosX
                    y2: model.object.clipInPosY
                }
            }

            property bool tmpConnectionExists : false
            property string tmpClipName
            property int tmpConnectionX1
            property int tmpConnectionY1
            property int tmpConnectionX2
            property int tmpConnectionY2

            CanvasConnection {
                id: tmpCanvasConnection
                visible: connections.tmpConnectionExists ? 1 : 0
                x1: connections.tmpConnectionX1
                y1: connections.tmpConnectionY1
                x2: connections.tmpConnectionX2
                y2: connections.tmpConnectionY2
            }
            MouseArea {
                anchors.fill: parent
                hoverEnabled:  true
                enabled: connections.tmpConnectionExists ? 1: 0
                onPositionChanged: {
                    if(connections.tmpConnectionExists){
                        if (connections.tmpClipName == "Output") {

                            tmpCanvasConnection.x2 = mouse.x - graphArea.originX
                            tmpCanvasConnection.y2 = mouse.y - graphArea.originY
                        }else{
                            tmpCanvasConnection.x1 = mouse.x - graphArea.originX
                            tmpCanvasConnection.y1 = mouse.y - graphArea.originY
                        }
                    }
                }
                onClicked: {
                    connections.tmpConnectionExists = false
                    tmpCanvasConnection.x2 = tmpCanvasConnection.x1
                    tmpCanvasConnection.y2 = tmpCanvasConnection.y1
                }
            }
        }

        //transform: Scale { id: scale; origin.x: graphArea.width/2; origin.y: graphArea.height/2; xScale: 1; yScale: 1}
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

    // NODE CREATION WITH RIGHT CLICK
    MouseArea {
        id: rightMouseArea
        anchors.fill: parent
        acceptedButtons: Qt.RightButton
        onClicked: {
            //_addMenu.showMenu(rightMouseArea.mouseX, rightMouseArea.mouseY);
            if (!tools.menuComponent) {
                if(rightMouseArea.mouseX + 500 < graph.width) {
                    var newComponent = Qt.createQmlObject('MenuList { parentName: "buttle/"; x: rightMouseArea.mouseX; y:  rightMouseArea.mouseY; clickFrom: graph; side: "right";}', parent);
                    //newComponent.side = "right";
                    tools.menuComponent = newComponent;
                    
                }
                else {
                    //var newComponent = Qt.createQmlObject('MenuList { parentName: "buttle/"; x: graph.width - 500; y:  rightMouseArea.mouseY; clickFrom: graph;}', parent);
                    var newComponent = Qt.createQmlObject('MenuList { parentName: "buttle/"; x: rightMouseArea.mouseX; y:  rightMouseArea.mouseY; clickFrom: graph; side: "left";}', parent);                    
                    //newComponent.side = "left";
                    tools.menuComponent = newComponent;     
                }
            }

                
             /*if (mouse.button == Qt.RightButton)
             listmodel.x = mouseX
             listmodel.y = mouseY - 30
             listmodel.clickFrom = graphArea
             listmodel.menuState = (listmodel.menuState == "hidden") ? "shown" : "hidden"
        }*/
        }   
    }
}

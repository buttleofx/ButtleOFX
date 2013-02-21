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

    DropArea {
        anchors.fill: parent
        onDrop: {
            if( hasUrls )
            {
                _buttleManager.dropReaderNode(firstUrl, pos.x, pos.y)
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
}

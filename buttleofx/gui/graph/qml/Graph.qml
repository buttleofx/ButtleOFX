import QtQuick 1.1
import ConnectionLineItem 1.0

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

    gradient: Gradient {
        GradientStop { position: 0.0; color: "#111111" }
        GradientStop { position: 0.015; color: "#212121" }
    }

    Rectangle {
        id: connectnode
        Item {
            id: nodes
            width: graphArea.width
            height: graphArea.height
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
            Repeater {
                model : _buttleData.graphWrapper.connectionWrappers
                ConnectionLine {
                    x1: model.object.clipOutPosX
                    y1: model.object.clipOutPosY
                    x2: model.object.clipInPosX
                    y2: model.object.clipInPosY
                }

            }

        }
    }

    MenuList {
        id: listmodel
    }   

    MouseArea{
        anchors.fill: parent
        acceptedButtons: Qt.MiddleButton 
        drag.target: connectnode
        drag.axis: Drag.XandYAxis
    } 

    /*MouseArea{
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
}

import QtQuick 1.1
import ConnectionLineItem 1.0

Rectangle {
    id:graphArea
    y: 30
    z: 0
    width: 850
    height: 350 - y

    gradient: Gradient {
        GradientStop { position: 0.0; color: "#111111" }
        GradientStop { position: 0.015; color: "#212121" }
    }

    Item{
        id: nodes
        width: parent.width
        height: parent.height
        Repeater {
            model : _buttleData.getGraphWrapper().getNodeWrappers()
            Node {
                Component.onDestruction: {
                    nodes.forceActiveFocus()
                }
            }
        }
    }


    Item{
    id: connections
    width: parent.width
    height: parent.height
        Repeater {

            model : _buttleData.getGraphWrapper().getConnectionWrappers()

                Item {
                    id: truc
                    property int coordX1 : model.object.clipOutPosX
                    property int coordY1 : model.object.clipOutPosY
                    property int coordX2 : model.object.clipInPosX
                    property int coordY2 : model.object.clipInPosY
                    width: (coordX2 - coordX1) > 0 ? (coordX2 - coordX1) : (coordX1 - coordX2)
                    height: (coordY2 - coordY1) > 0 ? (coordY2 - coordY1) : (coordY1 - coordY2)

                    ConnectionLine {
                        anchors.fill: parent
                        x1: coordX1
                        y1: coordY1
                        x2: coordX2
                        y2: coordY2
                    }
                    Component.onCompleted: {
                        console.log(truc.width);
                        console.log(truc.height);
                    }
               }
        }
    }


    MouseArea{
        anchors.fill: parent
        acceptedButtons: Qt.MiddleButton
        //drag.target: rect
        drag.target: nodes
        drag.axis: Drag.XandYAxis
    } 
}

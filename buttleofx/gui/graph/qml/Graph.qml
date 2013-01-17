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
            ConnectionLine {
                anchors.fill: parent
                x1: model.object.clipOutPosX
                y1: model.object.clipOutPosY
                x2: model.object.clipInPosX
                y2: model.object.clipInPosY
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

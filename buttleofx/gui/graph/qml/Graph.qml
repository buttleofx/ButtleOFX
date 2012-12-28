import QtQuick 1.1

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
            model : _nodeWrappers
            Node {}
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

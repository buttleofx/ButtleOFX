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
            model : _nodeWrappers
            Node {}
        }
    }


    Item{
    id: connections
    width: parent.width
    height: parent.height
        Repeater {
            model : _connectionWrappers
            ConnectionLine {
                id: connectionLine
                x1: _graphWrapper.getNode(model.object.clipOut._nodeName).coord[0]
                y1: _graphWrapper.getNode(model.object.clipOut._nodeName).coord[1]
                x2: _graphWrapper.getNode(model.object.clipIn._nodeName).coord[0]
                y2: _graphWrapper.getNode(model.object.clipIn._nodeName).coord[1]
                /*x1: 50
                y1: 50
                x2: 200
                y2: 200*/
            }
        }
    }

/*
    ConnectionLine {
        x1: 50
        y1: 50
        x2: 200
        y2: 200
    }
    ConnectionLine {
        x1: 80
        y1: 50
        x2: 150
        y2: 30
    }
*/
    MouseArea{
        anchors.fill: parent
        acceptedButtons: Qt.MiddleButton
        //drag.target: rect
        drag.target: nodes
        drag.axis: Drag.XandYAxis
    } 
}

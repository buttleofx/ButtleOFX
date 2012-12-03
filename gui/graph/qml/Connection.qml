import QtQuick 1.1

Rectangle {
    id: connection
    width: 100
    height: 2
    nodeIn: nodeIn
    nodeOut: nodeOut

    MouseArea {
        anchors.fill: parent
        drag.target: parent
        drag.axis: Drag.XandYAxis
    }
}

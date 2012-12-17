import QtQuick 1.1

Rectangle {
    id: connection
    implicitWidth: 100
    implicitHeight: 2
    nodeIn: nodeIn
    nodeOut: nodeOut

    MouseArea {
        anchors.fill: parent
        drag.target: parent
        drag.axis: Drag.XandYAxis
    }
}

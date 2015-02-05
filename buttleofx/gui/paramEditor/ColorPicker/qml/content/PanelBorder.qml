import QtQuick 2.0

Rectangle {
    id: root

    border.width: 1
    border.color: "#999999"
    color: "transparent"

    Rectangle {
        anchors.fill: parent
        radius: root.radius
        anchors.leftMargin: -root.border.width
        anchors.topMargin: -root.border.width
        anchors.rightMargin: 0
        anchors.bottomMargin: 0

        border.width: root.border.width ;
        border.color: Qt.lighter(root.border.color)
        color: "transparent"
    }
}

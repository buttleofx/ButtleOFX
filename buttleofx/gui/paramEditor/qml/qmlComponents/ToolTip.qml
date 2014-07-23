import QtQuick 2.0

Item {
    id: tooltip
    anchors.fill: parent
    property string paramHelp

    Rectangle {
        id: rectangle
        color: "#D8D9CB"
        border.width: 1
        border.color: "#333"
        radius: 3
        width: text.contentWidth
        height: text.contentHeight
        y: -height+10
    }

    Text{
        id: text
        color: "black"
        text: paramHelp
        width: 250
        wrapMode: Text.Wrap
        x: rectangle.x
        y: rectangle.y
    }
}

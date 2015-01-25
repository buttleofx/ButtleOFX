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
        radius: 2
        width: text.contentWidth + 4
        height: text.contentHeight + 4
        y: -height/2
    }

    Text{
        id: text
        color: "black"
        text: paramHelp
        width: 250
        wrapMode: Text.Wrap
        x: rectangle.x + 2
        y: rectangle.y
    }
}

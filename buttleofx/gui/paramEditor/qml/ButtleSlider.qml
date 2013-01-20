import QtQuick 1.1

Item {
    id: slider
    implicitWidth : 200
    implicitHeight : 20
    /*Text{
        id: minValue
        anchors.verticalCenter: parent.verticalCenter
        text: "0"//minValue in the future
        font.family: "Helvetica"
        font.pointSize: 8
        color: "red"
    }*/ 
    Text{
        id: currentValue
        anchors.horizontalCenter: parent.horizontalCenter
        text: cursorSlider.x + cursorSlider.width/2
        font.family: "Helvetica"
        font.pointSize: 8
        color: "white"
        y:-10
    }
    Rectangle {
        id: barSlider
        anchors.verticalCenter: parent.verticalCenter
        width: parent.width
        height: 2
        Rectangle{
            id: whiteBar
            x: barSlider.x
            width: cursorSlider.x - barSlider.x 
            height: parent.height
            color: "white"
        }
        Rectangle{
            id: greyBar
            x: barSlider.x + cursorSlider.x
            width: barSlider.width - whiteBar.width
            height: parent.height
            color: "grey"
        }
    }
    Rectangle {
        id: cursorSlider
        anchors.verticalCenter: parent.verticalCenter
        x: barSlider.x - cursorSlider.width/2
        height: 10
        width: 5
        radius: 1
        color: "white"
        MouseArea{
            anchors.fill: parent
            drag.target: parent
            drag.axis: Drag.XAxis
            drag.minimumX: barSlider.x - cursorSlider.width/2
            drag.maximumX: barSlider.x + barSlider.width - cursorSlider.width/2
            anchors.margins: -10 // allow to have an area around the cursor which allows to select the cursor even if we are not exactly on it
        }
    }
    Text{
        id: maxValue
        x: barSlider.x + barSlider.width + 5
        anchors.verticalCenter: parent.verticalCenter
        text: barSlider.width - barSlider.x//will be the real max value in the future
        font.pointSize: 8
        color: "white"
    }
}
import QtQuick 1.1

Item {
    id: slider
    implicitWidth : 200
    implicitHeight : 20

    property variant paramObject: model.object

    Row{
        id: paramSliderContainer
        spacing: 10

        /* Title of the paramSlider */
        Text {
            id: paramIntTitle
            text: paramObject.text + " : "
            color: "white"
        }
        /* The current value of the slider */
        Text{
            id: currentValue
            anchors.horizontalCenter: parent.horizontalCenter
            //text: cursorSlider.x + cursorSlider.width/2
            text: paramObject.value
            font.family: "Helvetica"
            font.pointSize: 8
            color: "white"
            y:-10
        }
        // bar slider : one grey, one white
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
        //cursor slider (little white rectangle)
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
                paramObject.value = (cursorSlider.x * paramObject.maximum) / barSlider.width
                console.log: paramObject.value
            }
        }
        // The max value (at the end of the bar slider)
        Text{
            id: maxValue
            x: barSlider.x + barSlider.width + 5
            anchors.verticalCenter: parent.verticalCenter
            text: paramObject.maximum
            font.pointSize: 8
            color: "white"
        }
    }
}
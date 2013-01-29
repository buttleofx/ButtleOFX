import QtQuick 1.1


Item {
    id: slider
    implicitWidth : 300
    implicitHeight : 30

    property variant paramObject: model.object

    Row{
        spacing: 10

        /* Title of the paramSlider */
        Text {
            id: paramDoubleTitle
            text: paramObject.text + " : "
            color: "white"
        }

        // The min value (at the beginning of the bar slider)
        Text{
            id: minValue
            text: paramObject.minimum
            font.pointSize: 8
            color: "white"
            y: 5
        }
        /* The current value of the slider */
        Item {
            width: 100
            height: parent.height
            Text{
                id: currentValue
                x: barSlider.width / 2
                text: paramObject.value
                font.family: "Helvetica"
                font.pointSize: 8
                color: "white"
                y:-8
            }
            // bar slider : one grey, one white
            Rectangle {
                id: barSlider
                width: 100
                height: 2
                y: 8
                Rectangle{
                    id: whiteBar
                    x: 0
                    width: cursorSlider.x
                    height: parent.height
                    color: "white"
                }
                Rectangle{
                    id: greyBar
                    x: cursorSlider.x
                    width: barSlider.width - whiteBar.width 
                    height: parent.height
                    color: "grey"
                }
            }
            // cursor slider (little white rectangle)
            Rectangle {
                id: cursorSlider
                x: ((paramObject.value - paramObject.minimum) * barSlider.width) / (paramObject.maximum - paramObject.minimum)
                y: 4
                height: 10
                width: 5
                radius: 1
                color: "white"
                MouseArea{
                    anchors.fill: parent
                    drag.target: parent
                    drag.axis: Drag.XAxis
                    drag.minimumX: 0// - cursorSlider.width/2
                    drag.maximumX: barSlider.width// - cursorSlider.width/2
                    anchors.margins: -10 // allow to have an area around the cursor which allows to select the cursor even if we are not exactly on it
                    onReleased: paramObject.value = (cursorSlider.x * (paramObject.maximum - paramObject.minimum)) / barSlider.width + paramObject.minimum
                    onXChanged: paramObject.value = (cursorSlider.x * (paramObject.maximum - paramObject.minimum)) / barSlider.width + paramObject.minimum 
                }
            }
        }
        // The max value (at the end of the bar slider)
        Text{
            id: maxValue
            text: paramObject.maximum
            font.pointSize: 8
            color: "white"
            y: 5
        }
    }
}
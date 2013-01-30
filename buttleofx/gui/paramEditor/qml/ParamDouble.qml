import QtQuick 1.1

Item {
    implicitWidth : 300
    implicitHeight : 30

    property variant paramObject: model.object

    /* Title of the paramSlider */
    Row {
        spacing: 10

        /* Title of the paramSlider */
        Text {
            id: paramIntTitle
            text: paramObject.text + " : "
            color: "white"
        }

        // The min value (at the beginning of the bar slider)
        Text {
            id: minValue
            text: paramObject.minimum
            font.pointSize: 8
            color: "white"
            y: 5
        }
        //The slider
        Item {
            width: 100
            height: parent.height

            // Current value
            TextInput {
                id: sliderInput
                width: barSlider.width / 2
                x: barSlider.width / 2 - width / 2
                y:-10
                horizontalAlignment: TextInput.AlignHCenter
                text: paramObject.value
                font.family: "Helvetica"
                font.pointSize: 8
                maximumLength: 5
                color: activeFocus ? "white" : "grey"
                activeFocusOnPress : true
                selectByMouse : true
                onAccepted: {
                    cursorSlider.x = ((sliderInput.text - paramObject.minimum) * barSlider.width) / (paramObject.maximum - paramObject.minimum);
                    paramObject.pushValue((cursorSlider.x * (paramObject.maximum - paramObject.minimum)) / barSlider.width + paramObject.minimum);
                }
                validator: DoubleValidator {
                    bottom: paramObject.minimum
                    top: paramObject.maximum
                }
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
                    color: "#00b2a1"
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
                radius: 2
                color: "white"
                MouseArea{
                    anchors.fill: parent
                    drag.target: parent
                    drag.axis: Drag.XAxis
                    drag.minimumX: 0// - cursorSlider.width/2
                    drag.maximumX: barSlider.width// - cursorSlider.width/2
                    anchors.margins: -10 // allow to have an area around the cursor which allows to select the cursor even if we are not exactly on it
                    onReleased: paramObject.pushValue((cursorSlider.x * (paramObject.maximum - paramObject.minimum)) / barSlider.width + paramObject.minimum)
                }
                onXChanged: paramObject.value = (cursorSlider.x * (paramObject.maximum - paramObject.minimum)) / barSlider.width + paramObject.minimum
            }
        }
        // The max value (at the end of the bar slider)
        Text {
            id: maxValue
            text: paramObject.maximum
            font.pointSize: 8
            color: "white"
            y: 5
        }
    }

}

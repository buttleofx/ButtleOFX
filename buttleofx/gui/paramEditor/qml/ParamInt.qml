import QtQuick 2.0

Item {
    id: paramInt
    implicitWidth : 300
    implicitHeight : 30
    y:10

    property variant paramObject: model.object

    // Is this param secret ?
    visible: !paramObject.isSecret
    height: paramObject.isSecret ? 0 : implicitHeight

    // To fix binding loops
    property bool mousePressed: false
    function updateXcursor() {
        return ((sliderInput.text - paramObject.minimum) * barSlider.width) / (paramObject.maximum - paramObject.minimum);
    }
    function updateTextValue() {
        return (cursorSlider.x * (paramObject.maximum - paramObject.minimum)) / barSlider.width + paramObject.minimum;
    }

    /* Title of the paramSlider */
    Row {
        spacing: 10

        /* Title of the paramSlider */
        Text {
            id: paramIntTitle
            text: paramObject.text + " : "
            color: "white"
            font.bold: paramObject.hasChanged ? true : false
            MouseArea {
                anchors.fill: parent
                acceptedButtons: Qt.RightButton
                onClicked: {
                    // reinitialise the param to its default value
                    paramObject.hasChanged = false
                    paramObject.value = paramObject.getDefaultValue()
                    paramObject.pushValue(paramObject.value)
                }
            }
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
                font.bold: paramObject.hasChanged ? true : false
                maximumLength: 8
                color: activeFocus ? "white" : "grey"
                //activeFocusOnPress : true
                selectByMouse : true
                validator: IntValidator {
                    bottom: paramObject.minimum
                    top: paramObject.maximum
                }
                onAccepted: {
                    //cursorSlider.x = updateXcursor();
                    paramObject.value = updateTextValue();
                    paramObject.pushValue(paramObject.value);
                }
                Component.onCompleted: {
                    cursorSlider.x = updateXcursor();
                }
                onTextChanged: {
                    if (!mousePressed) {
                        cursorSlider.x = updateXcursor();
                    }
                }
                onActiveFocusChanged: {
                    paramObject.value = updateTextValue();
                    paramObject.pushValue(paramObject.value);
                }
                MouseArea {
                    anchors.fill: parent
                    acceptedButtons: Qt.RightButton
                    onClicked: {
                        // reinitialise the param to its default value
                        paramObject.hasChanged = false
                        paramObject.value = paramObject.getDefaultValue()
                        paramObject.pushValue(paramObject.value)
                    }
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
                Rectangle {
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
                    onPressed: {
                        mousePressed = true
                        // take the focus
                        paramInt.forceActiveFocus()
                    }
                    onReleased: {
                        paramObject.value = updateTextValue()
                        paramObject.pushValue(paramObject.value);
                        mousePressed = false
                    }
                }
                onXChanged: {
                    if(mousePressed) {
                        paramObject.value = updateTextValue();
                    }
                }
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




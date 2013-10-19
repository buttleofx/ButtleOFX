import QtQuick 2.0
import "colorPickerComponents"
import "colorPickerComponents/ColorFunctions.js" as ColorFunctions

//set of tools to choose the color (square + slider color + color inputs)
Item{
    id: colorPicker

    property color colorValue: ColorFunctions.hsba(colorSlider.value, colorSelector.saturation, colorSelector.brightness, 1)
    property color colorSelectorValue: ColorFunctions.hsba(colorSlider.value, 1, 1, 1)


    implicitWidth: 267
    implicitHeight: 140
    //color: "transparent"

    property variant paramObject: model.object

    // Is this param secret ?
    visible: !paramObject.isSecret
    height: paramObject.isSecret ? 0 : implicitHeight

    Column {
        Text {
            id: titleColorPicker
            color: "white"
            //text: paramObject.text
        }

        Row{
            spacing: 5

            ColorSelector{
                id: colorSelector
                height: colorPicker.height
                width: height
                currentColor: colorSelectorValue
            }
            ColorSlider{
                id: colorSlider
                height: colorPicker.height
                //cursorColorPositionSlider: (colorInputs.cursorColorPositionInputs)/765 * colorPicker.height
            }
            ColorInputsRGB{
                id: colorInputs
                height: colorPicker.height
                currentColor: colorPicker.colorValue
                // if we try to implement that as a property of colorPicker, we have no more capital letters...
                redValue: ColorFunctions.getChannelStr(colorPicker.colorValue, 0)
                greenValue: ColorFunctions.getChannelStr(colorPicker.colorValue, 1)
                blueValue: ColorFunctions.getChannelStr(colorPicker.colorValue, 2)
                hValue: colorSlider.value.toFixed(2)
                sValue: colorSelector.saturation.toFixed(2)
                bValue: colorSelector.brightness.toFixed(2)
            }
        }
    }
}
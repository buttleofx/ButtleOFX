import QtQuick 1.1
import "colorPickerComponents"
import "colorPickerComponents/ColorFunctions.js" as ColorFunctions

Rectangle{
    id: colorPicker

    property color colorValue: ColorFunctions.hsba(colorSlider.value, colorSelector.saturation, colorSelector.brightness, alphaSlider.value)
    property color alphaColorText: ColorFunctions.fullColorString(colorPicker.colorValue, alphaSlider.value)

    implicitWidth: 267
    implicitHeight: 140
    color: "transparent"

    Row{
        anchors.fill: parent
        spacing: 5

        ColorSelector{
            id: colorSelector
            height: parent.height
            width: height
            currentColor: colorValue
        }
        ColorSlider{
            id: colorSlider
            height: parent.height
        }
        AlphaSlider{
            id: alphaSlider
            height: parent.height
        }
        ColorInputs{
            id: colorInputs
            height: parent.height
            currentColor: colorPicker.colorValue
            // if we try to implement that as a property of colorPicker, we have no more capital letters...
            alphaColorText: ColorFunctions.fullColorString(colorPicker.colorValue, alphaSlider.value)
            redValue: ColorFunctions.getChannelStr(colorPicker.colorValue, 0)
            greenValue: ColorFunctions.getChannelStr(colorPicker.colorValue, 1)
            blueValue: ColorFunctions.getChannelStr(colorPicker.colorValue, 2)
            hValue: colorSlider.value.toFixed(2)
            sValue: colorSelector.saturation.toFixed(2)
            bValue: colorSelector.brightness.toFixed(2)
            alphaValue: Math.ceil(alphaSlider.value*255)
        }
    }
}






import QtQuick 1.1
import "colorPickerComponents"
import "colorPickerComponents/ColorFunctions.js" as ColorFunctions

//set of tools to choose the color (square + slider color + slider alpha + color inputs)
Item{
    id: colorPicker

    property color colorValue: ColorFunctions.hsba(colorSlider.value, colorSelector.saturation, colorSelector.brightness, alphaSlider.value)
    property color alphaColorText: ColorFunctions.fullColorString(colorPicker.colorValue, alphaSlider.value)
    property color colorSelectorValue: ColorFunctions.hsba(colorSlider.value, 1, 1, 1)

    implicitWidth: 267
    implicitHeight: 200

    property variant paramObject: model.object

    Column {
        spacing: 10
        Text {
            id: titleColorPicker
            color: "white"
            text: paramObject.text
            height: 15
        }

        Row{
            spacing: 5

            ColorSelector{
                id: colorSelector
                height: colorPicker.height - titleColorPicker.height - 20
                width: height
                currentColor: colorSelectorValue
            }
            ColorSlider{
                id: colorSlider
                height: colorPicker.height - titleColorPicker.height - 20
                // test for enter colors values in inputs and adapt display
                // cursorColorPositionSlider: (colorInputs.cursorColorPositionInputs)/765 * colorPicker.height
            }
            AlphaSlider{
                id: alphaSlider
                height: colorPicker.height - titleColorPicker.height - 20
                cursorAlphaPositionSlider: alphaSlider.height - (colorInputs.cursorAlphaPositionInputs)/255 * alphaSlider.height
            }
            ColorInputsRGBA{
                id: colorInputs
                height: colorPicker.height - titleColorPicker.height - 20
                currentColor: colorPicker.colorValue
                alphaColorText: ColorFunctions.fullColorString(colorPicker.colorValue, alphaSlider.value)
                //redValue: paramObject.r //ColorFunctions.getChannelStr(colorPicker.colorValue, 0)
                //greenValue: paramObject.g //ColorFunctions.getChannelStr(colorPicker.colorValue, 1)
                //blueValue: paramObject.b //ColorFunctions.getChannelStr(colorPicker.colorValue, 2)
                alphaValue: Math.ceil(alphaSlider.value*255)
                hValue: colorSlider.value.toFixed(2)
                sValue: colorSelector.saturation.toFixed(2)
                bValue: colorSelector.brightness.toFixed(2)

            }
        }
    }
}
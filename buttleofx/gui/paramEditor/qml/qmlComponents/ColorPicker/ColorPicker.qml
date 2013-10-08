import QtQuick 1.1
import "colorPickerComponents"
import "colorPickerComponents/ColorFunctions.js" as ColorFunctions
import QuickMamba 1.0

//set of tools to choose the color (square + slider color + slider alpha + color inputs)
Item{
    id: colorPicker

    // creation of a signal used to prevent paramRGBA.qml when the color has changed
    signal mainColorChanged

    property color colorValue //Should be delete in the future

    property alias title: titleColorPicker.text //defined in ParamRGBA

    //property bool initialisationOfObject : true //first passage in the file
    property real defaultValueRed
    property real defaultValueGreen
    property real defaultValueBlue
    property real defaultValueAlpha

    ColorExtended {
        id: extendedColor
        entireColor: colorValue //entireColor is a property (a QColor) exposed in colorExtended from Quickmamba
        // others properties are accessible as hue, saturation, value, alpha
        Component.onCompleted : {
                red = defaultValueRed
                green = defaultValueGreen
                blue = defaultValueBlue
                alpha = defaultValueAlpha
        }
        // Maybe it's better to divide the signal in 4 (onRedChanged, onGreenChanged...?)
        onEntireColorChanged: {
            // signal capted in paramRGBA.qml, meaning we send informations to Tuttle
            colorPicker.mainColorChanged()
        }
    }

    // value which is used as the common value of inputs and cursors' positions, not modified directly
    property color currentColor

    // properties created just because we can't do currentColor.alpha, alpha is a property of a ColorExtended object....
    property real currentBrightness // brigthness also named value (v) in hsv color model
    property real currentSaturation
    property real currentHue 
    property real currentAlpha 

    // Every time the color changed we update the value of the properties
    onMainColorChanged :{
        currentColor = extendedColor.entireColor // used to give the color to Tuttle from ParamRGBA
        currentAlpha = extendedColor.alpha
        currentHue = extendedColor.hue
        currentSaturation = extendedColor.saturation
        currentBrightness = extendedColor.brightness
    }

    implicitWidth: 267
    implicitHeight: 200


    Column {
        spacing: 10
        Text {
            id: titleColorPicker
            color: "white"
            height: 15
        }

        Row {
            spacing: 5

            // Brightness (also named Value) / Saturation
            BrightnessAndSaturationSelector{
                id: colorSelector
                height: colorPicker.height - titleColorPicker.height - 20
                width: height
                currentColor: extendedColor ? ColorFunctions.hsba(extendedColor.hue, 1, 1, 1) : "black"
                saturation: currentSaturation
                brightness: currentBrightness

                /* doing an onNewSaturationChanged implies problems (because happens at the same time as onNewBrigthnessChanged ?)
                onNewSaturationChanged: {
                    extendedColor.saturation = newSaturation
                }*/

                onNewBrightnessChanged: {
                    // doing an onNewSaturationChanged implies problems (because the two signals happen at the same time ?)
                    extendedColor.brightness = newBrightness
                    extendedColor.saturation = newSaturation
                }
            }

            // Hue
            HueSlider{
                id: hueSlider
                height: colorPicker.height - titleColorPicker.height - 20
                /* when the color is white hue value is -1.0 so to avoid that the cursor of hueSlider goes out the colorPicker, we put
                the value to 0.0 */
                hue: currentHue >= 0.0 ? currentHue : 0.0
                onNewHueChanged: {
                    extendedColor.hue = newHue
                }
            }

            // Alpha
            AlphaSlider{
                id: alphaSlider
                height: colorPicker.height - titleColorPicker.height - 20
                // alphaValue takes the value of "currentColor.alpha" alias currentAlpha, it's useful if the value has been changed through the input text to update the position of the cursor
                alphaValue: currentAlpha
                onNewAlphaValueChanged: {
                    extendedColor.alpha = newAlphaValue
                }
            }

            // Text Inputs for colors (r, g, b and a)
            ColorInputsRGBA{
                id: colorInputs
                height: colorPicker.height - titleColorPicker.height - 20

                // values of inputs adapt them according to the value of the color
                currentColor: extendedColor ? extendedColor.entireColor : "black"
                alphaColorText: extendedColor ? ColorFunctions.fullColorString(extendedColor.entireColor, extendedColor.alpha) : "FFFFFFFF"
                redInput: extendedColor ? Math.ceil(extendedColor.red*255) : 255
                greenInput: extendedColor ? Math.ceil(extendedColor.green*255) : 255
                blueInput: extendedColor ? Math.ceil(extendedColor.blue*255) : 255
                alphaInput: extendedColor ? Math.ceil(extendedColor.alpha*255) : 255


                // newAlphaInput, newRedInput, newGreenInput, newBlueInput are defined in ColorInputsRGBA.qml
                // every time the value of an input changes, the color is updated
                onNewRedInputChanged: {
                    if(extendedColor)
                        extendedColor.red = newRedInput
                }

                onNewGreenInputChanged: {
                    if(extendedColor)
                        extendedColor.green = newGreenInput
                }

                onNewBlueInputChanged: {
                    if(extendedColor)
                        extendedColor.blue = newBlueInput
                }
                onNewAlphaInputChanged: {
                    if(extendedColor)
                        extendedColor.alpha = newAlphaInput
                }
            }
        }
    }
}
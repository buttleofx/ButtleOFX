import QtQuick 2.0
import "qmlComponents/ColorPicker"
import QuickMamba 1.0

ColorPicker {
    id: paramRGBA

    // colorObject ensures the link between qml and python
    property variant colorObject: model.object
    hasAlpha: false

    Component.onCompleted: {
        defaultValueRed = colorObject.r
        defaultValueGreen = colorObject.g
        defaultValueBlue = colorObject.b
        defaultValueAlpha = 1.0
    }

    title: colorObject.text

    // Is this param secret ?
    visible: !colorObject.isSecret
    height: colorObject.isSecret ? 0 : implicitHeight

    /*we can't directly write selectedColor.alpha because selectedColor
    is a color which is not the object colorExtended, so for the moment we do
    this trick and declare a colorExtended in paramRGBA too*/
    ColorExtended {
        id: mainCurrentColor
        // currentColor is a property of ColorPicker.qml
        entireColor: currentColor //entireColor is a QColor exposed in colorExtended from Quickmamba
    }


    // everytime the color changed, we send the data to Tuttle
    onMainColorChanged: {
        if(colorObject){
            colorObject.r = mainCurrentColor.red
            colorObject.g = mainCurrentColor.green
            colorObject.b = mainCurrentColor.blue
            //setValue is given from python in rgbaWrapper.py
            //colorObject.setValue(mainCurrentColor.red, mainCurrentColor.green, mainCurrentColor.blue, mainCurrentColor.alpha)
        }
    }
}

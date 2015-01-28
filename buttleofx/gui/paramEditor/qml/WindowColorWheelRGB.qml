import QtQuick 2.0
import QtQuick.Window 2.1
import QuickMamba 1.0
import "../ColorPicker/qml"

Window {

    width: 700
    height: 600
    color: "#212121"
    title: "Buttle OFX RGB ColorPicker"

    ColorPicker {
        id: paramRGB

        // colorObject ensures the link between qml and python
        property variant colorObject: model.object

        hasAlpha: false

        Component.onCompleted: {
            colorRGBA.x = colorObject.r
            colorRGBA.y = colorObject.g
            colorRGBA.z = colorObject.b
            colorRGBA.w = 1
        }

        // Everytime the color is changed, we send the data to Tuttle
        onAccepted: {
            if (colorObject) {
                colorObject.r = colorRGBA.x
                colorObject.g = colorRGBA.y
                colorObject.b = colorRGBA.z
                // setValue is given from python in rgbWrapper.py
                // colorObject.setValue(mainCurrentColor.red, mainCurrentColor.green, mainCurrentColor.blue)
            }
        }
    }
    onClosing: {
        openWindowRGB.isOpen = false
    }
}

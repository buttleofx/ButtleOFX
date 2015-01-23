import QtQuick 2.0
import QtQuick.Window 2.1
import QuickMamba 1.0
import "../ColorPicker/qml"

Window {

    width: 700
    height: 600
    color: "#212121"

    ColorPicker {
        id: paramRGBA

        // colorObject ensures the link between qml and python
        property variant colorObject: model.object

        Component.onCompleted: {
            colorRGBA.x = colorObject.r
            colorRGBA.y = colorObject.g
            colorRGBA.z = colorObject.b
            colorRGBA.w = colorObject.a
        }

        // Is this param secret?
        visible: !colorObject.isSecret
        height: colorObject.isSecret ? 0 : implicitHeight

        // Everytime the color is changed, we send the data to Tuttle
        onAccepted: {
            if (colorObject) {
                colorObject.r = colorRGBA.x
                colorObject.g = colorRGBA.y
                colorObject.b = colorRGBA.z
                colorObject.a = colorRGBA.w
                // setValue is given from python in rgbaWrapper.py
                // colorObject.setValue(mainCurrentColor.red, mainCurrentColor.green, mainCurrentColor.blue, mainCurrentColor.alpha)
            }
        }
    }
}

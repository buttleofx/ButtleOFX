import QtQuick 2.0
import "ColorUtils.js" as ColorUtils

Rectangle
{
    id: root
    color: "blue"

    property vector4d colorRGBA
    property vector4d colorHSVA

    // Call each time the value change
    signal colorChange(vector4d rgba)
    // Call when the user valids his choice (ex: mouse up)
    signal accepted

    Wheel {
        anchors.fill: parent
        anchors.margins: 10

        hue: colorHSVA.x
        saturation: colorHSVA.y

        onHueSaturationChange:{
            colorChange(ColorUtils.hsva2rgba(Qt.vector4d(hueSignal, saturationSignal, root.colorHSVA.z, root.colorHSVA.w)))
        }
        onAccepted: {
            root.accepted() ;
        }
    }
}

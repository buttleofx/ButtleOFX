import QtQuick 2.0
import QtQuick.Layouts 1.1
import "ColorUtils.js" as ColorUtils

ColumnLayout
{
    id: root

    property vector4d colorRGBA
    property vector4d colorHSVA
    property string mode

    // Call each time the value change
    signal colorChange(vector4d rgba)
    // Call when the user valids his choice (ex: mouse up)
    signal accepted

    Item {
        Layout.fillHeight: true
        Layout.fillWidth: true

        Wheel {
            anchors.fill: parent
            visible : root.mode === "Wheel"

            hue: root.colorHSVA.x
            saturation: root.colorHSVA.y

            onHueSaturationChange: colorChange(ColorUtils.hsva2rgba(Qt.vector4d(updatedHue, updatedSaturation, root.colorHSVA.z, root.colorHSVA.w)))
            onAccepted: root.accepted() ;
        }

        Rainbow {
            anchors.fill: parent
            visible : root.mode === "Rainbow"

            hue: root.colorHSVA.x
            luminance: root.colorHSVA.z ;

            onHueLuminanceChange:{
                colorChange(ColorUtils.hsva2rgba(Qt.vector4d(updatedHue, root.colorHSVA.y, updatedLuminance, root.colorHSVA.w)))
            }
            onAccepted: root.accepted() ;
        }

        SquareHuedColors {
            anchors.fill: parent
            visible : root.mode === "Square"

            colorHSV: Qt.vector3d(root.colorHSVA.x, root.colorHSVA.y, root.colorHSVA.z)

            onSaturationLuminanceChange:{
                colorChange(ColorUtils.hsva2rgba(Qt.vector4d(root.colorHSVA.x, updatedSaturation, updatedLuminance, root.colorHSVA.w)))
            }
            onAccepted: root.accepted() ;
        }
    }
}

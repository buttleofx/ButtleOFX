import QtQuick 2.0
import QtQuick.Controls 1.1
import QtQuick.Layouts 1.1
import "ColorUtils.js" as ColorUtils

ColumnLayout
{
    id: root

    property vector4d colorRGBA
    property vector4d colorHSVA

    // Call each time the value change
    signal colorChange(vector4d rgba)
    // Call when the user valids his choice (ex: mouse up)
    signal accepted

    RowLayout {
        spacing: 5
        Text {
            id:textMode
            text: "Mode :"
            color: "white"
        }

        ComboBox {
            id: modelList
            model : ["Wheel", "Rainbow", "Square"]
        }
    }

    Item {
        Layout.fillHeight: true
        Layout.fillWidth: true

        Wheel {
            anchors.fill: parent
            visible : modelList.model[modelList.currentIndex] === "Wheel"

            hue: root.colorHSVA.x
            saturation: root.colorHSVA.y

            onHueSaturationChange: colorChange(ColorUtils.hsva2rgba(Qt.vector4d(updatedHue, updatedSaturation, root.colorHSVA.z, root.colorHSVA.w)))
            onAccepted: root.accepted() ;
        }

        Rainbow {
            anchors.fill: parent
            visible : modelList.model[modelList.currentIndex] === "Rainbow"

            hue: root.colorHSVA.x
            luminance: { return root.colorHSVA.z ; console.debug("change") ; }

            onHueLuminanceChange:{
                console.debug("signal "+updatedHue+" "+updatedLuminance)
                colorChange(ColorUtils.hsva2rgba(Qt.vector4d(updatedHue, root.colorHSVA.y, updatedLuminance, root.colorHSVA.w)))
            }
            onAccepted: root.accepted() ;
        }
    }
}

import QtQuick 2.0
import QtQuick.Layouts 1.1
import "ColorUtils.js" as ColorUtils
import QtQuick.Controls 1.1
import QtQuick.Controls.Styles 1.1
import "../." // Qt-BUG import qmldir to use config singleton

TabView {
    id: root
    anchors.margins: 20
    property vector4d colorRGBA
    property vector4d colorHSVA
    property string mode

    // Call each time the value change
    signal colorRGBUpdate(vector4d rgba)
    signal colorHSVUpdate(vector4d hsva)
    // Call when the user valids his choice (ex: mouse up)
    signal accepted

    style: TabViewStyle {
        frameOverlap: 1
        frame: Rectangle {
            color: Config.backgroundColor
            border.width: Config.borderWidth
            border.color: Config.borderColor
        }
    }

    Tab {
        title: "Wheel"
        Item
        {
            anchors.fill: parent
            anchors.margins: 15
            Wheel {
                anchors.fill: parent

                hue: root.colorHSVA.x
                saturation: root.colorHSVA.y

                onHueSaturationChange: colorHSVUpdate(Qt.vector4d(updatedHue, updatedSaturation, root.colorHSVA.z, root.colorHSVA.w))
                onAccepted: root.accepted() ;
            }
        }
    }

    Tab {
        title: "Rainbow"
        Item
        {
            anchors.fill: parent
            anchors.margins: 15
            Rainbow {
                anchors.fill: parent

                hue: root.colorHSVA.x
                luminance: root.colorHSVA.z ;

                onHueLuminanceChange:{
                    colorHSVUpdate(Qt.vector4d(updatedHue, root.colorHSVA.y, updatedLuminance, root.colorHSVA.w))
                }
                onAccepted: root.accepted() ;
            }
        }
    }

    Tab {
        title: "Square"
        Item
        {
            anchors.fill: parent
            anchors.margins: 15
            SquareHuedColors {
                anchors.fill: parent

                colorHSV: Qt.vector3d(root.colorHSVA.x, root.colorHSVA.y, root.colorHSVA.z)

                onSaturationLuminanceChange:{
                    colorHSVUpdate(Qt.vector4d(root.colorHSVA.x, updatedSaturation, updatedLuminance, root.colorHSVA.w))
                }
                onAccepted: root.accepted() ;
            }
        }
    }
}

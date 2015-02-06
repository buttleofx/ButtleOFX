import QtQuick 2.0
import "ColorUtils.js" as ColorUtils
import QtQuick.Layouts 1.1
import QuickMamba 1.0

Item {
    id: root
    property vector4d colorRGBA
    property vector4d colorHSVA
    property int precision
    property bool hasAlpha: true

    // Call each time the value change
    signal colorRGBUpdate(vector4d rgba)
    signal colorHSVUpdate(vector4d hsva)
    // Call when the user valids his choice (ex: mouse up)
    signal accepted

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 8

        //*** RGB ***//

        // RED
        Channel {
            Layout.fillWidth: true
            Layout.maximumHeight: 40

            caption: "R"
            value: root.colorRGBA.x
            min: 0
            max: 255
            // Change to create the hue gradient
            toColor: Qt.vector4d(0, root.colorRGBA.y, root.colorRGBA.z,
                             root.colorRGBA.w)
            fromColor: Qt.vector4d(1, root.colorRGBA.y, root.colorRGBA.z,
                               root.colorRGBA.w)
            precision: root.precision

            onUpdatedValue: root.colorRGBUpdate(Qt.vector4d(updatedValue,
                                                         root.colorRGBA.y,
                                                         root.colorRGBA.z,
                                                         root.colorRGBA.w))
            onAccepted: root.accepted()
        }

        // GREEN
        Channel {
            Layout.fillWidth: true
            Layout.maximumHeight: 40

            caption: "G"
            value: root.colorRGBA.y
            // Change to create the hue gradient
            toColor: Qt.vector4d(root.colorRGBA.x, 0, root.colorRGBA.z,
                             root.colorRGBA.w)
            fromColor: Qt.vector4d(root.colorRGBA.x, 1, root.colorRGBA.z,
                               root.colorRGBA.w)
            precision: root.precision

            onUpdatedValue: root.colorRGBUpdate(Qt.vector4d(root.colorRGBA.x,
                                                         updatedValue,
                                                         root.colorRGBA.z,
                                                         root.colorRGBA.w))
            onAccepted: root.accepted()
        }

        // BLUE
        Channel {
            Layout.fillWidth: true
            Layout.maximumHeight: 40

            caption: "B"
            value: root.colorRGBA.z
            // Change to create the hue gradient
            toColor: Qt.vector4d(root.colorRGBA.x, root.colorRGBA.y, 0,
                             root.colorRGBA.w)
            fromColor: Qt.vector4d(root.colorRGBA.x, root.colorRGBA.y, 1,
                               root.colorRGBA.w)
            precision: root.precision

            onUpdatedValue: root.colorRGBUpdate(Qt.vector4d(root.colorRGBA.x,
                                                         root.colorRGBA.y,
                                                         updatedValue,
                                                         root.colorRGBA.w))
            onAccepted: root.accepted()
        }

        //*** HSV ***//

        // HUE
        Channel {
            Layout.fillWidth: true
            Layout.maximumHeight: 40

            caption: "H"

            value: root.colorHSVA.x

            gradient: HueGradient { opacity: root.colorHSVA.w }
            precision: root.precision

            onUpdatedValue: root.colorHSVUpdate(Qt.vector4d(updatedValue,
                                                             root.colorHSVA.y,
                                                             root.colorHSVA.z,
                                                             root.colorHSVA.w))
            onAccepted: root.accepted()
        }

        // SATURATION
        Channel {
            Layout.fillWidth: true
            Layout.maximumHeight: 40

            caption: "S"
            value: root.colorHSVA.y
            toColor: ColorUtils.hsva2rgba(Qt.vector4d(root.colorHSVA.x, 0,
                                            root.colorHSVA.z, root.colorHSVA.w))
            fromColor: ColorUtils.hsva2rgba(Qt.vector4d(root.colorHSVA.x, 1,
                                              root.colorHSVA.z,
                                              root.colorHSVA.w))
            precision: root.precision

            onUpdatedValue: root.colorHSVUpdate(Qt.vector4d(root.colorHSVA.x,
                                                             updatedValue,
                                                             root.colorHSVA.z,
                                                             root.colorHSVA.w))
            onAccepted: root.accepted()
        }

        // VALUE
        Channel {
            Layout.fillWidth: true
            Layout.maximumHeight: 40

            caption: "V"
            value: root.colorHSVA.z
            toColor: ColorUtils.hsva2rgba(Qt.vector4d(root.colorHSVA.x, root.colorHSVA.y,
                                            0, root.colorHSVA.w))
            fromColor: ColorUtils.hsva2rgba(Qt.vector4d(root.colorHSVA.x,
                                              root.colorHSVA.y, 1,
                                              root.colorHSVA.w))
            precision: root.precision

            onUpdatedValue: root.colorHSVUpdate(Qt.vector4d(root.colorHSVA.x,
                                                             root.colorHSVA.y,
                                                             updatedValue,
                                                             root.colorHSVA.w))
            onAccepted: root.accepted()
        }

        // ALPHA
        Channel {
            Layout.fillWidth: true
            Layout.maximumHeight: 40
            visible: root.hasAlpha

            caption: "A"
            value: root.colorRGBA.w
            toColor: Qt.vector4d(root.colorRGBA.x, root.colorRGBA.y,
                             root.colorRGBA.z, 0)
            fromColor: Qt.vector4d(root.colorRGBA.x, root.colorRGBA.y,
                               root.colorRGBA.z, 1)
            gradientAlpha: true
            precision: root.precision

            onUpdatedValue: root.colorRGBUpdate(Qt.vector4d(root.colorRGBA.x,
                                                         root.colorRGBA.y,
                                                         root.colorRGBA.z,
                                                         updatedValue))
            onAccepted: root.accepted()
        }
    }
}

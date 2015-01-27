import QtQuick 2.0
import "ColorUtils.js" as ColorUtils
import QtQuick.Layouts 1.1
import QuickMamba 1.0

Item {
    id: root
    property vector4d colorRGBA
    property vector4d colorHSVA
    property int precision
    property bool hasAlpha

    // Call each time the value change
    signal colorChange(vector4d rgba)
    // Call when the user valids his choice (ex: mouse up)
    signal accepted

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 8

        RowLayout {
            Layout.minimumHeight: 44
            Layout.maximumHeight: 60
            Layout.alignment: Layout.Center

            HexaInput {
                Layout.fillHeight: true

                colorRGB: Qt.vector3d(root.colorRGBA.x, root.colorRGBA.y,
                                      root.colorRGBA.z)
                onUpdatedColor: root.colorChange(Qt.vector4d(rgb.x, rgb.y, rgb.z,
                                                             root.colorRGBA.w))
            }

            ScreenPicker {
                Layout.fillHeight: true
                onAccepted: root.accepted()
                onGrabbedColor: {
                    var rgbColor = ColorUtils.hexa2rgb(color)
                    root.colorChange(Qt.vector4d(rgbColor.x, rgbColor.y, rgbColor.z, root.colorRGBA.w))
                }
            }
        }

        //*** RGB ***//

        // RED
        Channel {
            Layout.fillWidth: true
            Layout.maximumHeight: 40

            caption: "R"
            value: root.colorRGBA.x
            // Change to create the hue gradient
            toColor: Qt.rgba(0, root.colorRGBA.y, root.colorRGBA.z,
                             root.colorRGBA.w)
            fromColor: Qt.rgba(1, root.colorRGBA.y, root.colorRGBA.z,
                               root.colorRGBA.w)
            precision: root.precision

            onUpdatedValue: root.colorChange(Qt.vector4d(updatedValue,
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
            toColor: Qt.rgba(root.colorRGBA.x, 0, root.colorRGBA.z,
                             root.colorRGBA.w)
            fromColor: Qt.rgba(root.colorRGBA.x, 1, root.colorRGBA.z,
                               root.colorRGBA.w)
            precision: root.precision

            onUpdatedValue: root.colorChange(Qt.vector4d(root.colorRGBA.x,
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
            toColor: Qt.rgba(root.colorRGBA.x, root.colorRGBA.y, 0,
                             root.colorRGBA.w)
            fromColor: Qt.rgba(root.colorRGBA.x, root.colorRGBA.y, 1,
                               root.colorRGBA.w)
            precision: root.precision

            onUpdatedValue: root.colorChange(Qt.vector4d(root.colorRGBA.x,
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
            gradient: HueGradient { }
            precision: root.precision

            onUpdatedValue: root.colorChange(ColorUtils.hsva2rgba(
                                                 Qt.vector4d(updatedValue,
                                                             root.colorHSVA.y,
                                                             root.colorHSVA.z,
                                                             root.colorHSVA.w)))
            onAccepted: root.accepted()
        }

        // SATURATION
        Channel {
            Layout.fillWidth: true
            Layout.maximumHeight: 40

            caption: "S"
            value: root.colorHSVA.y
            toColor: ColorUtils.hsva2QtHsla(root.colorHSVA.x, 0,
                                            root.colorHSVA.z, root.colorHSVA.w)
            fromColor: ColorUtils.hsva2QtHsla(root.colorHSVA.x, 1,
                                              root.colorHSVA.z,
                                              root.colorHSVA.w)
            precision: root.precision

            onUpdatedValue: root.colorChange(ColorUtils.hsva2rgba(
                                                 Qt.vector4d(root.colorHSVA.x,
                                                             updatedValue,
                                                             root.colorHSVA.z,
                                                             root.colorHSVA.w)))
            onAccepted: root.accepted()
        }

        // VALUE
        Channel {
            Layout.fillWidth: true
            Layout.maximumHeight: 40

            caption: "V"
            value: root.colorHSVA.z
            toColor: ColorUtils.hsva2QtHsla(root.colorHSVA.x, root.colorHSVA.y,
                                            0, root.colorHSVA.w)
            fromColor: ColorUtils.hsva2QtHsla(root.colorHSVA.x,
                                              root.colorHSVA.y, 1,
                                              root.colorHSVA.w)
            precision: root.precision

            onUpdatedValue: root.colorChange(ColorUtils.hsva2rgba(
                                                 Qt.vector4d(root.colorHSVA.x,
                                                             root.colorHSVA.y,
                                                             updatedValue,
                                                             root.colorHSVA.w)))
            onAccepted: root.accepted()
        }

        // ALPHA
        Channel {
            Layout.fillWidth: true
            Layout.maximumHeight: 40
            visible: root.hasAlpha

            caption: "A"
            value: root.colorRGBA.w
            toColor: Qt.rgba(root.colorRGBA.x, root.colorRGBA.y,
                             root.colorRGBA.z, 0)
            fromColor: Qt.rgba(root.colorRGBA.x, root.colorRGBA.y,
                               root.colorRGBA.z, 1)
            precision: root.precision

            onUpdatedValue: root.colorChange(Qt.vector4d(root.colorRGBA.x,
                                                         root.colorRGBA.y,
                                                         root.colorRGBA.z,
                                                         updatedValue))
            onAccepted: root.accepted()
        }
    }


}

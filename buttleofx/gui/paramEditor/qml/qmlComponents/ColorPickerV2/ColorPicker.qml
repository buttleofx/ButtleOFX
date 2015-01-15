import QtQuick 2.2
import QtQuick.Window 2.0
import QtQuick.Layouts 1.1
import "content"
import "content/ColorUtils.js" as ColorUtils

Item {
    id: root
    anchors.fill: parent

    // Color value in RGBA with floating point values between 0.0 and 1.0.
    property vector4d colorRGBA: Qt.vector4d(1, 1, 1, 1)
    QtObject {
        id: m
        // Color value in HSVA with floating point values between 0.0 and 1.0.
        property vector4d colorHSVA:  ColorUtils.rgba2hsva(root.colorRGBA)
    }

    signal accepted()
    onAccepted: console.debug("UPDATE TUTLE")

    ColumnLayout {
        anchors.fill: parent

        RowLayout {
            Layout.minimumHeight: 150

            ColorRepresentation {
                id:colorRepresentation
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.minimumWidth: 150

                colorRGBA: root.colorRGBA
                colorHSVA: m.colorHSVA

                onColorChange: {
                    // rgba comes from signal
                    root.colorRGBA.x = rgba.x
                    root.colorRGBA.y = rgba.y
                    root.colorRGBA.z = rgba.z
                }
                onAccepted: root.accepted()
            }

            ChannelsEditor {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.minimumWidth: 350
                color: "orange"

                colorRGBA: root.colorRGBA
                colorHSVA: m.colorHSVA

                onColorChange: {
                    // rgba comes from signal
                    root.colorRGBA = rgba
                }
            }
        }

        RowLayout {

            ColorVisualisation {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.minimumHeight: 50
                Layout.minimumWidth: 150
                color: Qt.rgba(root.colorRGBA.x, root.colorRGBA.y, root.colorRGBA.z, root.colorRGBA.w)
            }
        }

    }
}

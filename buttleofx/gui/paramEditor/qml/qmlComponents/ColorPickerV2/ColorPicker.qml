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


    onColorRGBAChanged: {
        var hsva = ColorUtils.rgba2hsva(root.colorRGBA);
        // When the color is a grey level color, we must conserve the lost hue and saturation by conversion
        if (root.colorRGBA.x == root.colorRGBA.y && root.colorRGBA.y == root.colorRGBA.z) {
            hsva.x = m.colorHSVA.x;
            hsva.y = m.colorHSVA.y;
        }
        m.colorHSVA = hsva;
    }

    QtObject {
        id: m
        // Color value in HSVA with floating point values between 0.0 and 1.0.
        // updated when RGBA change
        property vector4d colorHSVA:  Qt.vector4d(1, 1, 1, 1)
    }

    signal accepted
    onAccepted: console.debug("UPDATE TUTLE")

    ColumnLayout {
        anchors.fill: parent

        RowLayout {

            // Display a shape representation as wheel, rainbow...
            ColorRepresentation {
                id:colorRepresentation
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.minimumWidth: 150                
                Layout.minimumHeight: 150

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

            // Give tool to edit precisely a color or a channel by text input, slider, picker...
            ChannelsEditor {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.minimumWidth: 150
                Layout.minimumHeight: 150
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
            // Display the color choosen and her complementary
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

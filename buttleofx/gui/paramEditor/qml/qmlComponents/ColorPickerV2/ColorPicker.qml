import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Layouts 1.1
import "content"
import "content/ColorUtils.js" as ColorUtils
import "content/mathUtils.js" as MathUtils

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
        property vector4d colorHSVA:  Qt.vector4d(0, 0, 1, 1)
    }

    signal accepted
    onAccepted: console.debug("UPDATE TUTLE")

    ColumnLayout {
        anchors.fill: parent

        RowLayout {
            Layout.maximumHeight: 20
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignHCenter
            spacing: 50

            RowLayout {
                Text {
                    id:textMode
                    text: "Mode : "
                    color: "white"
                }

                ComboBox {
                    id: modelList
                    model : ["Wheel", "Rainbow", "Square"]
                }
            }

            NumberBox {
                Layout.maximumWidth: 150

                id:precisionBox
                min: 0
                max: 30
                decimals: 0
                value:5
                caption : "Precision : "

                onAccepted: precisionBox.value = updatedValue
            }
        }

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
                mode: modelList.currentText

                onColorChange: {
                    // rgba comes from signal
                    rgba.x = MathUtils.decimalRound(rgba.x, precisionBox.value)
                    rgba.y = MathUtils.decimalRound(rgba.y, precisionBox.value)
                    rgba.z = MathUtils.decimalRound(rgba.z, precisionBox.value)
                    rgba.w = MathUtils.decimalRound(rgba.w, precisionBox.value)
                    root.colorRGBA = rgba
                }
                onAccepted: root.accepted()
            }


            // Give tool to edit precisely a color or a channel by text input, slider, picker...
            ChannelsEditor {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.minimumWidth: 150
                Layout.minimumHeight: 150

                colorRGBA: root.colorRGBA
                colorHSVA: m.colorHSVA
                precision: precisionBox.value

                onColorChange: {
                    // rgba comes from signal
                    rgba.x = MathUtils.decimalRound(rgba.x, precisionBox.value)
                    rgba.y = MathUtils.decimalRound(rgba.y, precisionBox.value)
                    rgba.z = MathUtils.decimalRound(rgba.z, precisionBox.value)
                    rgba.w = MathUtils.decimalRound(rgba.w, precisionBox.value)
                    root.colorRGBA = rgba
                }
                onAccepted: root.accepted()
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

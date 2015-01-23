import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Layouts 1.1
import "content"
import "content/ColorUtils.js" as ColorUtils
import "content/mathUtils.js" as MathUtils
import "." // Qt-BUG import qmldir to use config singleton

Item {
    id: root
    anchors.fill: parent
    anchors.margins: parent.width * 0.01

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
            Layout.preferredHeight: 20
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignHCenter
            spacing: parent.width * 0.1

            RowLayout {
                Text {
                    id:textMode
                    text: "Mode : "

                    font.family: Config.font
                    font.pixelSize: Config.textSize
                    color: Config.textColor
                }

                ComboBox {
                    id: modelList
                    model : ["Wheel", "Rainbow", "Square"]
                }
            }

            NumberBox {                
                id:precisionBox
                Layout.maximumWidth: 150
                Layout.maximumHeight: 40
                min: 1
                max: 15
                decimals: 0
                value:5
                caption : "Precision : "

                textInput.font.family: Config.font
                textInput.font.pixelSize: Config.textSize
                textInput.color: Config.textColor
                textInput.horizontalAlignment: TextInput.AlignHCenter
                text.font.family: Config.font
                text.font.pixelSize: Config.textSize
                text.color: Config.textColor

                onUpdatedValue: precisionBox.value = newValue
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

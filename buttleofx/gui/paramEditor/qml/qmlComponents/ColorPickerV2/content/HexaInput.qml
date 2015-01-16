import QtQuick 2.2
import QtQuick.Layouts 1.1
import "ColorUtils.js" as ColorUtils

RowLayout {
    id:root

    property vector3d colorRGB

    signal updatedColor(var rgb)

    spacing: 5

    // Wrap text by item because text have a bad behaviour in Layout
    Item {
        Layout.fillHeight: true
        Layout.minimumWidth: captionBox.font.pixelSize

        Text {
            id: captionBox
            anchors.centerIn: parent

            text: "#"
            color: "#AAAAAA"
            font.pixelSize: parent.height / 2
            font.bold: true
        }
    }

    PanelBorder {
        Layout.fillHeight: true
        Layout.minimumWidth: hexaColor.maximumLength * hexaColor.font.pixelSize

        TextInput {
            id: hexaColor

            anchors.centerIn: parent
            color: "#AAAAAA"
            selectionColor: "#FF7777AA"
            font.pixelSize: parent.height / 2
            font.capitalization: "AllUppercase"
            font.family: "TlwgTypewriter"
            selectByMouse: true
            focus: true

            text: ColorUtils.rgb2hexa(Qt.vector3d(root.colorRGB.x, root.colorRGB.y, root.colorRGB.z))
            maximumLength: 6
            validator: RegExpValidator {
                regExp: /^([A-Fa-f0-9]{6})$/
            }

            onEditingFinished: {
                root.updatedColor( Qt.vector3d(parseInt(text.substr(0, 2),16) / 255,
                                           parseInt(text.substr(2, 2),16) / 255,
                                           parseInt(text.substr(4, 2),16) / 255) )
            }
        }
    }
}

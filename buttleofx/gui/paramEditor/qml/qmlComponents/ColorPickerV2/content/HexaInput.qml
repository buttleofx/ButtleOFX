import QtQuick 2.2
import QtQuick.Layouts 1.1
import "ColorUtils.js" as ColorUtils
import "../." // Qt-BUG import qmldir to use config singleton

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
            font.family: Config.font
            font.pixelSize: Config.textSize
            font.bold: false
            color: Config.textColor
        }
    }

    PanelBorder {
        Layout.fillHeight: true
        Layout.minimumWidth: hexaColor.maximumLength * hexaColor.font.pixelSize

        TextInput {
            id: hexaColor

            anchors.centerIn: parent
            font.family: Config.font
            font.pixelSize: Config.textSize
            font.bold: false
            color: Config.textColor
            font.capitalization: "AllUppercase"
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

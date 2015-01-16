import QtQuick 2.2
import QtQuick.Layouts 1.1
import "ColorUtils.js" as ColorUtils
import "mathUtils.js" as MathUtils

RowLayout {
    id: root

    property string caption: ""
    property real value: 0
    property real min: 0
    property real max: 255
    property int decimals: 5

    signal accepted(var updatedValue)

    QtObject {
        id: m
        // Hack: force update of the text after text validation
        property int forceTextUpdate: 0
    }

    spacing: 5

    // Wrap text by item because text have a bad behaviour in Layout
    Item {
        Layout.fillHeight: true
        Layout.minimumWidth: captionBox.font.pixelSize

        Text {
            id: captionBox
            anchors.centerIn: parent

            text: root.caption
            color: "#AAAAAA"
            font.pixelSize: parent.height / 2
            font.bold: true
        }
    }


    PanelBorder {
        Layout.fillHeight: true
        Layout.minimumWidth: (root.max.toString().length + root.decimals + 1) * inputBox.font.pixelSize

        TextInput {
            id: inputBox
            // Hack: force update of the text if the value is the same after the clamp.
            text: m.forceTextUpdate ? MathUtils.decimalRound(root.value, root.decimals) : MathUtils.decimalRound(root.value, root.decimals)

            anchors.centerIn: parent
            color: "#AAAAAA"
            selectionColor: "#FF7777AA"
            font.pixelSize: parent.height / 2
            font.family: "TlwgTypewriter"
            focus: true

            onEditingFinished: {
                var newText = MathUtils.clamp(parseFloat(inputBox.text), root.min, root.max).toString()
                if(newText != root.value && newText !== NaN) {
                    root.accepted(MathUtils.decimalRound(newText, root.decimals))
                }
                else {
                    m.forceTextUpdate = m.forceTextUpdate + 1 // Hack: force update
                }
            }
        }
    }
}



import QtQuick 2.2
import QtQuick.Layouts 1.1
import "ColorUtils.js" as ColorUtils
import "mathUtils.js" as MathUtils
import "../." // Qt-BUG import qmldir to use config singleton
import "../../../../../../../QuickMamba/qml/QuickMamba"

RowLayout {
    id: root

    // Alias to configure style of text from external
    property alias textInput: inputBox.textInput
    property alias text: captionBox

    property string caption: ""
    property real captionWidth: captionBox.contentWidth
    property real value: 0
    property real min: 0
    property real max: 255
    property int decimals: 5

    signal accepted(var updatedValue)

    function updateValue(newValue)
    {
        var newText = MathUtils.clamp(newValue, root.min, root.max).toString()
        if(newText != root.value && newText !== NaN) {
            root.accepted(MathUtils.decimalRound(newText, root.decimals))
        }
        else {
            m.forceTextUpdate = m.forceTextUpdate + 1 // Hack: force update
        }
    }

    QtObject {
        id: m
        // Hack: force update of the text after text validation
        property int forceTextUpdate: 0
    }

    Text {
        Layout.minimumWidth: captionWidth
        id: captionBox
        text: root.caption
        color: "#AAAAAA"
    }

    QuickEditableNumberInput {
        id: inputBox

        Layout.fillHeight: true
        Layout.fillWidth: true
        // Hack: force update of the text if the value is the same after the clamp.
        textInput.text: m.forceTextUpdate ? MathUtils.decimalRound(root.value, root.decimals) : MathUtils.decimalRound(root.value, root.decimals)

        border.width: Config.borderWidth
        border.color: Config.borderColor
        radius: Config.radius
        color: Config.backgroundColor
        cursorColor: Config.accentColor

        onQuickUpdate: root.updateValue(quickValue)
        textInput.onAccepted: root.updateValue(parseFloat(inputBox.textInput.text))
    }
}




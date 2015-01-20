import QtQuick 2.0
import QtQuick.Layouts 1.1

RowLayout
{
    id: root

    property real value
    property color fromColor
    property color toColor
    property string caption
    property int precision

    signal updatedValue(var updatedValue)
    signal accepted

    spacing: 5

    NumberBox {
        id: numberbox
        Layout.fillHeight: true
        Layout.maximumWidth: (decimals + 2) * textInput.font.pixelSize
        Layout.minimumWidth: decimals / 2 * textInput.font.pixelSize

        value: root.value
        decimals: root.precision
        max: 1
        min: 0
        caption: root.caption

        onAccepted: {
            root.updatedValue(updatedValue);
            root.accepted();
        }
    }


    HorizontalColorSlider
    {
        id: horizontalColorSlider
        Layout.fillHeight: true
        Layout.fillWidth: true
        Layout.minimumWidth: 50

        value: root.value
        fromColor: root.fromColor
        toColor: root.toColor

        onUpdatedValue: root.updatedValue(updatedValue)
        onAccepted: root.accepted()
    }
}

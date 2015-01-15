import QtQuick 2.0
import QtQuick.Layouts 1.1

RowLayout
{
    id: root

    property real value
    property color fromColor
    property color toColor
    property string caption

    signal updatedValue(var updatedValue)
    signal accepted

    NumberBox {
        id: numberbox
        Layout.fillWidth: true
        Layout.fillHeight: true

        // TODO: put in NumberBox
        value: root.value // 5 Decimals
        decimals: 2
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
        Layout.fillWidth: true
        Layout.fillHeight: true

        value: root.value
        fromColor: root.fromColor
        toColor: root.toColor

        onUpdatedValue: root.updatedValue(updatedValue)
        onAccepted: root.accepted()
    }
}

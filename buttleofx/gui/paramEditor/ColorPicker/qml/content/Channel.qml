import QtQuick 2.0
import QtQuick.Layouts 1.1
import "mathUtils.js" as MathUtils
import "../." // Qt-BUG import qmldir to use config singleton

RowLayout
{
    id: root

    property real min : 0
    property real max : 1
    property int precision
    // Value should always be in [0 - 1]
    property real value

    property string caption
    property vector4d fromColor: Qt.vector4d(0, 0, 0, 1)
    property vector4d toColor: Qt.vector4d(0, 0, 0, 1)
    // Or for other special gradient use :
    property alias gradient: horizontalColorSlider.gradient
    property bool gradientAlpha: false

    signal updatedValue(var updatedValue)
    signal accepted

    spacing: parent.width * 0.02

    NumberBox {
        id: numberbox
        Layout.fillHeight: true
        Layout.maximumWidth: (decimals + 4) * textInput.font.pixelSize + 15
        Layout.minimumWidth: (decimals + 4) / 2 * textInput.font.pixelSize + 15

        value: MathUtils.clampAndProject(root.value, 0, 1, root.min, root.max)
        //If interval is not 0-1 so no precision needed
        decimals: root.max > 1 ? 0 : root.precision
        max: root.max
        min: root.min
        caption: root.caption
        captionWidth: Config.textSize

        text.font.family: Config.font
        text.font.pixelSize: Config.textSize
        text.font.bold: false
        text.color: Config.textColor
        textInput.font.family: Config.font
        textInput.font.pixelSize: Config.textSize
        textInput.color: Config.textColor
        textInput.horizontalAlignment: TextInput.AlignHCenter

        onUpdatedValue: root.updatedValue(MathUtils.clampAndProject(newValue, root.min, root.max, 0, 1));

        onAccepted: {
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
        gradientAlpha: root.gradientAlpha

        onUpdatedValue: root.updatedValue(updatedValue)
        onAccepted: root.accepted()
    }
}

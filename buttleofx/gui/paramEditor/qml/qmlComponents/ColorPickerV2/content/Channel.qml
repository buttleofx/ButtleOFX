import QtQuick 2.0
import QtQuick.Layouts 1.1
import "../." // Qt-BUG import qmldir to use config singleton

RowLayout
{
    id: root

    property real value
    property string caption
    property int precision    
    property color fromColor
    property color toColor
    // Or for other special gradient use :
    property alias gradient: horizontalColorSlider.gradient

    signal updatedValue(var updatedValue)
    signal accepted

    spacing: parent.width * 0.02

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
        captionWidth: Config.textSize

        text.font.family: Config.font
        text.font.pixelSize: Config.textSize
        text.font.bold: false
        text.color: Config.textColor
        textInput.font.family: Config.font
        textInput.font.pixelSize: Config.textSize
        textInput.color: Config.textColor
        textInput.horizontalAlignment: TextInput.AlignHCenter

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

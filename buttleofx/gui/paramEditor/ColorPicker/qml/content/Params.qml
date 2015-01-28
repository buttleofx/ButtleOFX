import QtQuick 2.0
import QtQuick.Layouts 1.1
import "../." // Qt-BUG import qmldir to use config singleton

Rectangle {
    id: root
    border.width: Config.borderWidth
    border.color: Config.borderColor
    radius: Config.radius
    color: Config.backgroundColor
    signal updatePrecision(var precision)

    property int precision : precisionBox.value
    MouseArea {
        anchors.fill: root
        hoverEnabled: true
        onEntered: root.visible = true
        onExited: root.visible = false
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 5 + root.border.width * 2

        NumberBox {
            id:precisionBox
            Layout.fillWidth: true
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





}

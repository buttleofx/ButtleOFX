import QtQuick 2.0
import QtQuick.Layouts 1.1
import QtQuick.Controls 1.1
import "../." // Qt-BUG import qmldir to use config singleton

Rectangle {
    id: root
    border.width: Config.borderWidth
    border.color: Config.borderColor
    radius: Config.radius
    color: Config.backgroundColor

    signal updatePrecision(var precision)
    signal entered()
    signal exited()

    property int precision: precisionBox.value
    property bool isZeroOneRange: rangeValue.currentText == "0-1"

    MouseArea {
        anchors.fill: root
        hoverEnabled: true
        onEntered: root.entered()
        onExited: root.exited()
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 5 + root.border.width * 2

        NumberBox {
            id:precisionBox
            Layout.fillWidth: true
            Layout.maximumHeight: 40
            min:0
            max: 15
            decimals: 0
            value: 5
            caption : "Precision : "

            textInput.readOnly: !isZeroOneRange
            textInput.font.family: Config.font
            textInput.font.pixelSize: Config.textSize
            textInput.color: Config.textColor
            textInput.horizontalAlignment: TextInput.AlignHCenter
            text.font.family: Config.font
            text.font.pixelSize: Config.textSize
            text.color: Config.textColor

            onUpdatedValue: precisionBox.value = newValue
        }

        RowLayout {

            Text {
                text: "Value : "
                font.family: Config.font
                font.pixelSize: Config.textSize
                color: Config.textColor
            }

            ComboBox {
                id: rangeValue
                model: ListModel {
                    ListElement { text: "0-1" }
                    ListElement { text: "0-255" }
                }
                // Hack because exit root area is triggered when enter on this comboBox
                onHoveredChanged: root.entered()

                onCurrentTextChanged: {
                    if (currentText == "0-1")
                        return precisionBox.value = 5;
                    else
                        // 0-255 int range need no more precision than 3 digits for final RGB value
                        return precisionBox.value = 3;
                }
            }
        }
    }
}

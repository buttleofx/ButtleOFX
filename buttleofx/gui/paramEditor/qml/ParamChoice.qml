import QtQuick 2.0
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0

Item {
    id: choiceList
    implicitWidth: 300
    implicitHeight: 30
    y: 5

    property variant paramObject: model.object
    // property variant menuItems: paramObject.listValue

    // Is this param secret?
    visible: !paramObject.isSecret
    height: paramObject.isSecret ? 0 : implicitHeight

    // Convert the QObjectListmodel into a qml ListModel
    ListModel {
        id: menuItems
    }

    Component.onCompleted: {
        for (var i = 0; i < paramObject.listValue.count; i++) {
            menuItems.append( {text: paramObject.listValue.get(i)} )
        }
    }

    Row {
        id: paramChoiceInputContainer
        spacing: 10
        clip: true

        // Title of the param
        Text {
            id: paramChoiceTitle
            text: paramObject.text + " : "
            color: "white"
            y: 5

            // If param has been modified, title in bold font
            font.bold: paramObject.hasChanged ? true : false

            MouseArea {
                anchors.fill: parent
                acceptedButtons: Qt.RightButton

                onClicked: {
                    paramObject.hasChanged = false
                    paramObject.value = paramObject.getDefaultValue()
                    paramObject.pushValue(paramObject.value)
                }
            }
        }

        ComboBox {
            id: comboBox
            model: menuItems
            width: 200
            height: 30

            style: ComboBoxStyle {
                background: Rectangle {
                    id: choiceButton
                    color: "#212121"
                    border.width: 1
                    border.color: "#333"
                    radius: 3

                    Image {
                        id: arrow
                        source: "file:///" + _buttleData.buttlePath + "/gui/img/buttons/params/arrow.png"
                        y: 12
                        x: 187
                    }
                }
                label: Text {
                    color: "white"
                    text: paramObject.value
                    width: comboBox.width
                    y: 2
                    x: -2
                    elide:Text.ElideRight
                }
            }

            // Useful to avoid setting paramObject.value when loaded the comboBox
            property int comboBoxCharged: 0

            currentIndex: paramObject.value

            onCurrentIndexChanged: {
                if (comboBoxCharged) {
                    paramObject.value = menuItems.get(currentIndex).text
                    paramObject.pushValue(paramObject.value)
                } else {
                    comboBoxCharged = 1
                }
            }
        }
    }
}

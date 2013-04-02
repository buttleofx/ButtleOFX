import QtQuick 1.1
import QtDesktop 0.1

Item {
    id: choiceList
    implicitWidth: 300
    implicitHeight: 30

    property variant paramObject: model.object

    // Is this param secret ?
    visible: !paramObject.isSecret
    height: paramObject.isSecret ? 0 : implicitHeight

    // convert the qobjectlistmodel into a qml ListModel
    ListModel {
        id: menuItems
    }
    Component.onCompleted: {
        for( var i=0; i < paramObject.listValue.count; i++ )
        {
            menuItems.append( {text: paramObject.listValue.get(i)} )
        }
    }

    Row {
        id: paramChoiceInputContainer
        spacing: 10

        //Title of the param
        Text {
            id: paramChoiceTitle
            text: paramObject.text + " : "
            color: "white"
            // if param has been modified, title in bold font
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
            y: -7

            // usefull to avoid setting paramObject.value when loaded the comboBox
            property int comboBoxCharged: 0

            selectedText: paramObject.value

            onSelectedIndexChanged: {
                if (comboBoxCharged) {
                    paramObject.value = menuItems.get(selectedIndex).text
                    paramObject.pushValue(paramObject.value)
                }
                else {
                    comboBoxCharged = 1
                }
            }
        }
    }
}

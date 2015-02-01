import QtQuick 2.0
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0

Item {
    id: choiceList
    implicitWidth: 300
    implicitHeight: 30

    property variant paramObject: model.object
    // property variant menuItems: paramObject.listValue

    // Convert the QObjectListmodel into a qml ListModel
    ListModel {
        id: menuItems
    }
    Component.onCompleted: {
        for (var i = 0; i < paramObject.listValue.count; i++) {
            menuItems.append( {text: paramObject.listValue.get(i)} )
        }
    }
    Item {
        anchors.fill: parent
        anchors.topMargin: 2
        anchors.bottomMargin: 2
        anchors.rightMargin: 30

        ComboBox {
            id: comboBox
            model: menuItems
            width: parent.width

            // TODO: RemoveClipping bug when click.
            //this bug come from the ComboBoxstyle
//            style: ComboBoxStyle {
//                background: Rectangle {
//                    id: choiceButton
//                    color: "#212121"
//                    border.width: 1
//                    border.color: "#333"
//                    radius: 3

//                    Image {
//                        id: arrow
//                        source: "file:///" + _buttleData.buttlePath + "/gui/img/buttons/params/arrow.png"
//                        anchors.right:parent.right
//                        anchors.rightMargin: 5
//                        y: 10
//                    }
//                }
//                label: Text {
//                    color: "white"
//                    text: paramObject.value
//                    width: comboBox.width
//                    y: 2
//                    x: -2
//                    elide:Text.ElideRight
//                }
//            }


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

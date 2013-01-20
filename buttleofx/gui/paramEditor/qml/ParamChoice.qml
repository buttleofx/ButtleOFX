import QtQuick 1.1
import QtDesktop 0.1

Item {
    id: choiceList
    implicitWidth: 300
    implicitHeight: 30
    property alias title: paramChoiceTitle.text

    Row {
        id: paramChoiceInputContainer
        spacing: 10

        //Title of the param
        Text {
            id: paramChoiceTitle
            width: 80
            text: model.object.text + " : "
            color: "white"
           // font.pointSize: 8
            anchors.top: parent.top
            anchors.verticalCenter: parent.verticalCenter
        }

        // List
        Item {
            height: 20
            width: 40

            ListModel {
                id: menuItems

                ListElement { text: "Constant" }
                ListElement { text: "Black"}
                ListElement { text: "Padded" }
            }

            ComboBox {
                model: menuItems
                width: 150
                height: 20
                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter
            } 
        }
    }       
}

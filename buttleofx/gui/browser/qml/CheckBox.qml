import QtQuick 2.0

FocusScope {
    id: checkbox

    Accessible.role: Accessible.CheckBox

    property string text: "CheckBox"
    property bool checked // required variable

    width: 100
    height: 30

    Row {
        spacing: 2

        Rectangle {
            width: 12
            height: 12
            border.width: checkbox.focus ? 2 : 1
            border.color: "black"

            Text {
                id: checkboxText
                text: checkbox.checked ? "x" : ""
                anchors.centerIn: parent
            }
        }

        Text {
            text: checkbox.text
        }
    }

    MouseArea {
        anchors.fill: parent
        onClicked: checkbox.checked = !checkbox.checked
    }

}
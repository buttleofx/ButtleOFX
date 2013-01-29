import QtQuick 1.1

Item {
    implicitWidth: 100
    implicitHeight: 20

    Row {
        spacing: 10
        Rectangle {
            width: 70
            height: 3
            color: "white"
            y: 8
        }

        /*Title of the param*/
        Text {
            id: paramGroupTitle
            text: object.label
            color: "white"
            font.pointSize: 15
        }

        Rectangle {
            width: 70
            height: 3
            color: "white"
            y: 8
        }
    }
}

import QtQuick 2.0

Item {
    implicitWidth: 100
    implicitHeight: 20

    property variant paramObject: model.object

    // Is this param secret?
    visible: !paramObject.isSecret
    height: paramObject.isSecret ? 0 : implicitHeight

    Row {
        spacing: 10
        Rectangle {
            width: 70
            height: 3
            color: "white"
            y: 8
        }

        // Title of the param
        Text {
            id: paramGroupTitle
            text: paramObject.label
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

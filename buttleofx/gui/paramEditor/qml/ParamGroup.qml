import QtQuick 1.1

Item {
    implicitWidth: 100
    implicitHeight: 30

    property variant paramObject: model.object

    // Is this param secret ?
    visible: !paramObject.isSecret
    height: paramObject.isSecret ? 0 : implicitHeight

    Row {
        spacing: 10
        Rectangle {
            width: 100
            height: 1
            color: "grey"
            y: 8
        }

        /*Title of the param*/
        Text {
            id: paramGroupTitle
            text: paramObject.label
            color: "white"
            font.pointSize: 11
        }

        Rectangle {
            width: 100
            height: 1
            color: "grey"
            y: 8
        }
    }
}

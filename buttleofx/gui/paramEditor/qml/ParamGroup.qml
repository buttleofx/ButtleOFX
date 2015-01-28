import QtQuick 2.0

Item {
    implicitWidth: 100
    implicitHeight: 30

    property variant paramObject: model.object

    // Is this param secret?
    visible: !paramObject.isSecret
    height: paramObject.isSecret ? 0 : implicitHeight

    Row {
        spacing: 10

        Rectangle {
            width: 200
            height: 1
            color: "grey"
            y: 15
        }
    }
}

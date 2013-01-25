import QtQuick 1.1

Item {
    implicitWidth: 100
    implicitHeight: 20

    property alias title: paramBooleanTitle.text
    property variant paramObject: model.object

    Row {
        id: paramBoleanInputContainer
        spacing: 10

        /*Title of the param*/
        Text {
            id: paramBooleanTitle
            text: paramObject.text + " : "
            color: "white"
        }

        /*Black square we can check*/
        Rectangle {
            id: box
            width: 15
            height: 15
            radius : 1
            color: "black"

            /*When we check, an other white square appears in the black one*/
            Rectangle{
                id: interiorBox
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.verticalCenter: parent.verticalCenter
                width: box.width - box.width/2
                height: width
                radius: 1
                state: paramObject.value ? "FOCUS_ON" : "FOCUS_OFF"

                states: [
                    State {
                        name: "FOCUS_OFF"
                        PropertyChanges { target: interiorBox; color: "black" }
                    },
                    State {
                        name: "FOCUS_ON"
                        PropertyChanges { target: interiorBox; color: "white" }
                    }
                ]
            }

            MouseArea{
                anchors.fill: parent
                onPressed: {
                    interiorBox.state = (interiorBox.state == "FOCUS_ON") ? "FOCUS_OFF" : "FOCUS_ON"
                    paramObject.value = (interiorBox.state == "FOCUS_ON") ? 1 : 0
                }
            }
        }
    }
}
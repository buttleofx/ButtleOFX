import QtQuick 1.1

Item {
    implicitWidth: 100
    implicitHeight: 30

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
            color: "#343434"
            border.width: 1
            border.color: "#444"

            /*When we check, an other white square appears in the black one*/
            Rectangle{
                id: interiorBox
                anchors.centerIn: parent
                width: box.width/2 + 1
                height: width
                radius: 1
                state: paramObject.value ? "FOCUS_ON" : "FOCUS_OFF"

                states: [
                    State {
                        name: "FOCUS_OFF"
                        PropertyChanges { target: interiorBox; color: "#343434" }
                    },
                    State {
                        name: "FOCUS_ON"
                        PropertyChanges { target: interiorBox; color: "#00b2a1" }
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
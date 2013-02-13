import QtQuick 1.1

Item {
    id: paramBoolean
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

                states: [
                    State {
                        when: paramObject.value == false
                        name: "FOCUS_OFF"
                        PropertyChanges { target: interiorBox; color: "#343434" }
                    },
                    State {
                        when: paramObject.value == true
                        name: "FOCUS_ON"
                        PropertyChanges { target: interiorBox; color: "#00b2a1" }
                    }
                ]
            }

            MouseArea{
                anchors.fill: parent
                onPressed: {
                    paramObject.value = (paramObject.value == false) ? true : false                    
                    paramObject.pushValue(paramObject.value)
                    // take the focus of the MainWindow
                    paramBoolean.forceActiveFocus()
                }
            }
        }
    }
}
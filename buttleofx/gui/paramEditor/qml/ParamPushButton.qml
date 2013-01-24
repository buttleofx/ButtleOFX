import QtQuick 1.1

Item {
    implicitWidth: 120
    implicitHeight: 30

    property variant paramObject: model.object

    Rectangle {
        id: pushButton
        width: 120
        height: 30
        color: "#212121"
        radius: 5
        border.width: 2
        border.color: "grey"

        property string label: paramObject.label
        property bool enabled:  paramObject.enabled

        state: paramObject.enabled ? "enabled" : "disnabled"

        Text {
            id: buttonid
            color: "white"
            text: parent.label
            anchors.centerIn: parent
            font.family: "Arial"
            font.pixelSize: 14

            Component.onCompleted:
            {
                pushButton.height = font.pixelSize + 6
            }
        }

        MouseArea {
            id: buttonmousearea
            anchors.fill: parent

            onPressed:
            {
                pushButton.state = (pushButton.state == "FOCUS_ON") ? "FOCUS_OFF" : "FOCUS_ON"
                paramObject.enabled = (pushButton.state == "FOCUS_ON") ? "True" : "False"
            }
        }

        states: [
            State {
                id: stateEnabled
                name: "enabled"; when: pushButton.enabled
                PropertyChanges { 
                    target: buttonid; 
                    color: "white";  
                }
            },
            State {
                id: stateDisnabled
                name: "disnabled"; when: !pushButton.enabled
                PropertyChanges { 
                    target: buttonid; 
                    color: "grey";  
                }
            }
        ]
    }
}
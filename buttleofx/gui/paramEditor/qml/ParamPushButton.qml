import QtQuick 2.0
import "qmlComponents"

Item {
    implicitWidth: 120
    implicitHeight: 30
    y:10

    property variant paramObject: model.object

    // Is this param secret ?
    visible: !paramObject.isSecret
    height: paramObject.isSecret ? 0 : implicitHeight

    Rectangle {
        id: pushButton
        width: 120
        height: 30
        color: "#343434"
        radius: 5
        border.width: 1
        border.color: "#444"

        property string name: paramObject.name
        property bool enabled:  paramObject.enabled

        state: paramObject.enabled ? "enabled" : "disabled"

        Text {
            id: buttonid
            color: "white"
            text: parent.name
            anchors.horizontalCenter: parent.horizontalCenter
            y: 2
            font.pixelSize: 14

            ToolTip{
                id:tooltip
                visible: false
                paramHelp:paramObject.doc
            }

            Component.onCompleted:
            {
                pushButton.height = font.pixelSize + 6
            }
        }

        MouseArea {
            id: buttonmousearea
            anchors.fill: parent
            hoverEnabled:true

            onPressed:
            {
                pushButton.state = (pushButton.state == "enabled" ? "disabled" : "enabled")
                // take the focus of the MainWindow
                pushButton.forceActiveFocus()
            }
            onEntered: {
                tooltip.visible=true
            }
            onExited: {
                tooltip.visible=false
            }
        }

        states: [
            State {
                id: stateEnabled
                name: "enabled"
                when: pushButton.enabled
                PropertyChanges { 
                    target: buttonid
                    color: "white"
                }
                PropertyChanges { 
                    target: pushButton 
                    color: "555"
                }
            },
            State {
                id: stateDisabled
                name: "disabled"
                when: !pushButton.enabled
                PropertyChanges { 
                    target: buttonid
                    color: "grey"
                }
                PropertyChanges { 
                    target: pushButton 
                    color: "#343434" 
                }
            }
        ]
    }
}

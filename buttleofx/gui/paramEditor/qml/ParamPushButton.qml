import QtQuick 1.1

Rectangle {
    id: pushButton
    width: 60
    height: 20
    color: "#d1cbcb"
    radius: 5
    border.width: 2
    border.color: "#00b2a1"

    property string label: model.object.label
    property string trigger : model.object.trigger
    property bool enabled:  model.object.enabled

    signal buttonpressed()

    function setEnabled(isenabled)
    {
        enabled = isenabled
    }

    Text {
        id: buttonid
        color: "black"
        text: label
        font.bold: false
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
            if (pushButton.enabled)
            {
                parent.color = "#ffffff"
            }
        }

        onReleased:
        {
            if (pushButton.enabled)
            {
                parent.color = "#d1cbcb"
            }
        }

        onClicked:
        {
            if (pushButton.enabled)
            {
                pushButton.buttonpressed(trigger)
            }
        }

    }

    states: [
    State {
        id: stateEnabled
        name: "enabled"; when: pushButton.enabled
        PropertyChanges { target: buttonid; color: "black";  }
    },
    State {
        id: stateDisnabled
        name: "disnabled"; when: !pushButton.enabled
        PropertyChanges { target: buttonid; color: "gray";  }
    }
    ]
}
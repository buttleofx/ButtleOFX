import QtQuick 1.1

Rectangle {
    id: clip
    property string port : parent.port

    height: clipSize
    width: clipSize
    color: "#bbbbbb"
    radius: 4

    MouseArea {
        id: clipMouseArea
        anchors.fill: parent
        anchors.margins: -8
        hoverEnabled: true
        onPressed: {
            color = "#018fff"
            _buttleData.clipPressed(m.nodeModel.name, port, index) // we send all information needed to identify the clip : nodename, port and clip number
            clip.forceActiveFocus()
        }
        onReleased: {
            color = "#bbbbbb"
             _buttleData.clipReleased(m.nodeModel.name, port, index)
        }
        onEntered: {
            color = "#00b2a1"
        }
        onExited: {
            color = "#bbbbbb"
        }
    }
}

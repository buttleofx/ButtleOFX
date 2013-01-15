import QtQuick 1.1

Rectangle {
    height: 5
    width: 5
    color: "#bbbbbb"
    radius: 2
    property string port : parent.port

    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        onPressed: {
            color = "red"
            _graphWrapper.clipPressed(m.nodeModel.name, port, index) // we send all information needed to identify the clip : nodename, port and clip number
        }
        onReleased: {
            color = "#bbbbbb"
             _graphWrapper.clipReleased(m.nodeModel.name, port, index)
        }
        onEntered: {
            color = "blue"
        }
        onExited: {
            color = "#bbbbbb"
        }
    }
}

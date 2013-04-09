import QtQuick 1.1
import QuickMamba 1.0

Rectangle {
    id: clip
    property string port
    property variant clipWrapper

    QtObject {
        id: c
        property variant clipModel: clipWrapper
    }

    height: clipSize
    width: clipSize
    color:  clipMouseArea.containsMouse ? "#00b2a1" : "#bbbbbb"
    radius: 4

    Rectangle {

        id: clipName
        color: clipMouseArea.containsMouse ? "#fff" : "#333"
        radius: 3
        opacity: clipMouseArea.containsMouse ? 1 : 0
        height: 17
        width: clipNameText.width + 10
        x: clip.port == "output" ? parent.x + 15 : parent.x - clipNameText.width - 15
        y: -5

        Text{
            id: clipNameText
            text: c.clipModel.name
            font.pointSize: 8
            color: "#999"
            x: 7
            y: 4
        }
    }



    DropArea {
        anchors.fill: parent
        anchors.margins: -7
        onDragEnter: {
            acceptDrop = hasText && text.substring(0, 5) == "clip/";

            // tmpConnection update
            if(acceptDrop) {
                // position of the clip
                var posClip = _buttleData.graphWrapper.getPointClip(c.clipModel.nodeName, c.clipModel.name, index)

                if (connections.tmpClipName == "Output") {
                    connections.tmpConnectionX2 =  posClip.x
                    connections.tmpConnectionY2 =  posClip.y
                }
                else {
                    connections.tmpConnectionX1 =  posClip.x
                    connections.tmpConnectionY1 =  posClip.y
//                }
            }
        }

        onDrop: {
            if (acceptDrop) {
                _buttleManager.connectionManager.connectionDropEvent(text, c.clipModel, index)
            }
        }
    }

    MouseArea {
        id: clipMouseArea
        anchors.fill: parent
        hoverEnabled: true

        onPressed: {
            // take the focus of the MainWindow
            clip.forceActiveFocus()

            // tmpConnection :
            // position of the clip
            var posClip = _buttleData.graphWrapper.getPointClip(c.clipModel.nodeName, c.clipModel.name, index)

            // display of the tmpConnection with right coordinates
            connections.tmpConnectionExists = true
            connections.tmpClipName = c.clipModel.name
            connections.tmpConnectionX1 = posClip.x
            connections.tmpConnectionY1 = posClip.y
            connections.tmpConnectionX2 = posClip.x
            connections.tmpConnectionY2 = posClip.y


            // drag execution
            _buttleManager.connectionManager.connectionDragEvent(c.clipModel, index) // we send all information needed to identify the clip : nodename, port and clip number

            // at the end of the drag (i.e. onReleased !), we hide the tmpConnection.
            connections.tmpConnectionExists = false
        }


       /*
            // Doesn't work because of the drag execution
            onReleased: { connections.tmpConnectionExists = false}
       */
    }
}

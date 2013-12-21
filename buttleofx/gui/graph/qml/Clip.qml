import QtQuick 2.0
import QuickMamba 1.0

Rectangle {
    id: clipRoot

    property string port
    property variant clipWrapper
    property variant graphRoot
    //nodeRoot est récupéré de Node.qml, il désigne le node auquel appartient le clip
    property variant nodeRoot

    QtObject {
        id: m
        property variant clipWrapper: clipRoot.clipWrapper
        property double radius: clipSize / 2.0
    }

    objectName: "qmlClip_" + m.clipWrapper.name
    height: clipSize
    width: clipSize
    color: clipMouseArea.containsMouse ? "#00b2a1" : "#bbbbbb"
    radius: 4

    // Synchronize QML graphic information (clip position) into the model,
    // to share it with connection objects
    property double absXPos: nodeRoot.x + clipRoot.mapToItem(nodeRoot, m.radius, m.radius).x // Est-ce la position du clip dans le repère du graph ?
    onAbsXPosChanged: {
        // console.debug("__________")
        // console.debug("clipRoot qml update clip coord:", absXPos)
        // console.debug("nodeRoot.x:", nodeRoot.x)
        // console.debug("clipRoot.x:", clipRoot.mapToItem(nodeRoot, m.radius, m.radius).x)
        // console.debug("m.radius:", m.radius)
        // console.debug("__________")
        clipWrapper.coord.x = absXPos
    }
    property double absYPos: nodeRoot.y + clipRoot.mapToItem(nodeRoot, m.radius, m.radius).y
    onAbsYPosChanged: {
        // console.debug("__________", m.clipWrapper.nodeName, m.clipWrapper.name)
        // console.debug("clipRoot qml update clip coord:", absYPos)
        // console.debug("nodeRoot.y:", nodeRoot.y)
        // console.debug("clipRoot.y:", clipRoot.mapToItem(nodeRoot, m.radius, m.radius).y)
        // console.debug("m.radius:", m.radius)
        // console.debug("__________")
        clipWrapper.coord.y = absYPos
    }
    function updateClipWrapperCoords()
    {
        clipWrapper.coord.x = absXPos
        clipWrapper.coord.y = absYPos
    }
    Component.onCompleted: {
        updateClipWrapperCoords()
    }

    Rectangle {
        id: clipName
        color: clipMouseArea.containsMouse ? "#fff" : "#333"
        radius: 3
        opacity: clipMouseArea.containsMouse ? 1 : 0
        height: 17
        width: clipNameText.width + 10
        x: clipRoot.port == "output" ? parent.x + 15 : parent.x - clipNameText.width - 15
        y: -5

        Text{
            id: clipNameText
            text: m.clipWrapper.name
            font.pointSize: 8
            color: "#999"
            x: 7
            y: 4
        }
    }

    DropArea {
        id: droparea
        objectName: "DropArea"
        width: 15
        height: 15
        keys: "handle"
        onDropped: {
            // Accepts the drop and erase the handle
            drop.accept()

            handle.state = ""

            var clipOut = null
            var clipIn = null
            console.log("clip.clipWrapper.name:", m.clipWrapper.name)
            if( m.clipWrapper.name == "Output" )
            {
                console.log("drop on output")
                clipOut = m.clipWrapper
                clipIn = drag.source.clipWrapper
            }
            else
            {
                console.log("drop on input")
                clipOut = drag.source.clipWrapper
                clipIn = m.clipWrapper

                console.log("clipOut:", clipOut)
                console.log("clipIn:", clipIn)
                console.log("drag.source:", drag.source)
            }
            _buttleManager.connectionManager.connectWrappers(clipOut, clipIn)
        }
        onEntered: { //The handle is displayed to show that a connection is available
            handle.state = "entereddrop"
        }
        onExited: { //Erase the handle
            handle.state = ""
        }
        Item { //Area that accepts the drop
            id: droprec
            width: 15
            height: 15
            x : -4
            y: -3
        }
    }

    //MouseArea dedicated to the QML drag and drop
    MouseArea {
        id: clipMouseArea
        anchors.fill: parent
        hoverEnabled: true
        drag.target: handle

        onReleased: {
            var dropStatus = handle.Drag.drop()
            if (dropStatus !== Qt.IgnoreAction)
                console.log("Accepted!")
            connections.tmpConnectionExists = false
            handle.opacity= 0
        }

        //invisble rectangle which is dragged from an output to an input
        Rectangle {
            id: handle
            width: 7
            height: 7
            radius: 4
            x: 0
            y: 0
            color: "#32d2cc"
            Drag.active: clipMouseArea.drag.active
            Drag.hotSpot.x: width * 0.5
            Drag.hotSpot.y: height * 0.5
            Drag.keys: "handle"
            opacity: 0
            property variant clipWrapper: m.clipWrapper
            states: [
                State {
                   name: "dragging"
                   when: handle.Drag.active
                   PropertyChanges {
                      target: handle
                      opacity: 1
                   }
                },
                State {
                   name: "entereddrop"
                   PropertyChanges {
                      target: handle
                      opacity: 0.5
                      radius: 8
                      width: 15
                      height: 15
                      x: -handle.width/4
                      y: -handle.height/4
                   }
                }
            ]
        }

        onPressed: {
            // take the focus of the MainWindow
            clipRoot.forceActiveFocus()
            // tmpConnection :
            // position of the clip
            var posClip = clipRoot.mapToItem(clipRoot.graphRoot, m.radius, m.radius)

            // display of the tmpConnection with right coordinates
            connections.tmpConnectionExists = true
            connections.tmpClipName = m.clipWrapper.name

            connections.tmpConnectionX1 = posClip.x
            connections.tmpConnectionY1 = posClip.y
            connections.tmpConnectionX2 = posClip.x
            connections.tmpConnectionY2 = posClip.y


       }
       onPositionChanged: {
           // Update of the connection during the drag
           if(clipMouseArea.drag.active) {
                if (connections.tmpClipName == "Output") {
                    connections.tmpConnectionX2 = mouse.x + connections.tmpConnectionX1
                    connections.tmpConnectionY2 = mouse.y + connections.tmpConnectionY1
                } else {
                    connections.tmpConnectionX1 = mouse.x + connections.tmpConnectionX2
                    connections.tmpConnectionY1 = mouse.y + connections.tmpConnectionY2
                }
           }
           handle.x = mouseX
           handle.y = mouseY
        }
    }
}

import QtQuick 2.0
import QuickMamba 1.0
import Viewport 1.0

Rectangle {
    id: container

    property url imageFile
    //property real time: 0
    //property int fps: 25
    property int frameViewer: 0
    color: "#111111"

    GLViewport {
        id: viewport
        anchors.fill: parent
        
        offset.x: 0.0
        offset.y: 0.0
        //frame is a QProperty defined in glviewport_tuttleofx.py
        frame: container.frameViewer//container.time/1000 * container.fps
        fittedMode: true

        property real inWidth: 16
        property real inHeight: 9
        property real inRatio: inWidth/inHeight

        property real outWidth: parent.width
        property real outHeight: parent.height
        property real ratioWidth: outWidth / inWidth
        property real ratioHeight: outHeight / inHeight
        property real fitOnWidth: ratioWidth > ratioHeight
        property real fitRatio: fitOnWidth ? ratioWidth : ratioHeight

        Component.onDestruction: {
            viewport.unconnectToButtleEvent()
        }

        MouseArea {
            anchors.fill: parent
            acceptedButtons: Qt.LeftButton | Qt.MiddleButton
            
            property real offsetXOnPress: 0
            property real offsetYOnPress: 0
            property real posXOnPress: 0
            property real posYOnPress: 0
            onPositionChanged: {
                var mouseOffsetX = (mouse.x - posXOnPress) / viewport.imgScale
                var mouseY = height-mouse.y
                var mouseOffsetY = (mouseY - posYOnPress) / viewport.imgScale
                viewport.setOffset_xy(
                    offsetXOnPress - mouseOffsetX,
                    offsetYOnPress - mouseOffsetY )
            }
            onPressed: {
                posXOnPress = mouse.x
                posYOnPress = (height-mouse.y)
                offsetXOnPress = viewport.offset.x
                offsetYOnPress = viewport.offset.y
                viewport.fittedMode = false
            }
            onDoubleClicked: {
                viewport.fitImage()
                viewport.fittedMode = true
            }
        }
        MouseArea {
            anchors.fill: parent
            property real nbSteps: 10
            onWheel: {
                var deltaF = (wheel.angleDelta.y / 120.0) / nbSteps
                var newScale = viewport.imgScale * (1.0 + deltaF)
                viewport.setScaleAtPos_viewportCoord( newScale, pos.x, (height-pos.y) )
                viewport.fittedMode = false
            }
        }
        /*DropArea {
            anchors.fill: parent
            
            onDrop: {
                if( hasUrls )
                {
                    //viewport.imageFilepath = firstUrl
                }
            }
        }*/
    }

}



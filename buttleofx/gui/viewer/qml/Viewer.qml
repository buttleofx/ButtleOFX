import QtQuick 1.1
import QuickMamba 1.0
import Viewport 1.0

Rectangle {
    id: container

    property url imageFile

    color:"#1e1e1e"

    GLViewport {
        id: viewport
        anchors.fill: parent
        
        offset.x: 0.0
        offset.y: 0.0
        fittedMode: true
        imageFilepath: parent.imageFile

        property real inWidth: 16
        property real inHeight: 9
        property real inRatio: inWidth/inHeight

        property real outWidth: parent.width
        property real outHeight: parent.height
        property real ratioWidth: outWidth / inWidth
        property real ratioHeight: outHeight / inHeight
        property real fitOnWidth: ratioWidth > ratioHeight
        property real fitRatio: fitOnWidth ? ratioWidth : ratioHeight

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
        WheelArea {
            anchors.fill: parent
            property real nbSteps: 10
            onVerticalWheel: {
                var deltaF = (delta / 120.0) / nbSteps
                var newScale = viewport.imgScale * (1.0 + deltaF)
                viewport.setScaleAtPos_viewportCoord( newScale, pos.x, (height-pos.y) )
                viewport.fittedMode = false
            }
        }
        DropArea {
            anchors.fill: parent
            
            onDrop: {
                if( hasUrls )
                {
                    viewport.imageFilepath = firstUrl
                }
            }
        }
    }

}



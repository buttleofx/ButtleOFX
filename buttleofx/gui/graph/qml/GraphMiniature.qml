import QtQuick 2.0
import QtQuick.Layouts 1.0
import QtQuick.Controls 1.0

Rectangle {
    id: root

    property vector4d graphBBox: _buttleData.graphWrapper.bbox

    function screenToWorld(pos){

    }

    MouseArea {
        id: miniatureArea
        anchors.fill: parent

        property vector2d startPos
        property bool isMovingViewport: false

        hoverEnabled: true
        acceptedButtons: Qt.LeftButton

        onPressed: {
            xStart = mouse.x
            yStart = mouse.y
            visuWindowXStart = tmpVisuWindow.x
            visuWindowYStart = tmpVisuWindow.y
            isMovingViewport = pressedButtons & Qt.LeftButton
        }
        onReleased: {
            if (isMovingViewport) {
                isMovingViewport = false
                root.tmpMode = false

                if (mouse.x>0 && mouse.x < root.width) {
                    root.xOffset = mouse.x - xStart
                } else if (mouse.x > root.width) {
                    root.xOffset = root.width - xStart
                } else {
                    root.xOffset = -xStart
                }

                if (mouse.y > 0 && mouse.y < root.height) {
                    root.yOffset = mouse.y - yStart
                } else if (mouse.y > root.height) {
                    root.yOffset = root.height - yStart
                } else {
                    root.yOffset = -yStart
                }

                root.miniOffsetX += root.xOffset
                root.miniOffsetY += root.yOffset
                // TODO: don't modify graph, use signal
                graph.container.x -= (root.xOffset/root.scaleFactor*graph.zoomCoeff)
                graph.container.y -= (root.yOffset/root.scaleFactor*graph.zoomCoeff)

                // To map the tmpVisuWindow (zoom)
                root.originX = visuWindow.x
                root.originY = visuWindow.y
                tmpVisuWindow.width = visuWindow.width
                tmpVisuWindow.height = visuWindow.height
            }
        }
        onPositionChanged: {
            /*
            if (isMovingViewport) {
                root.tmpMode = true

                if ((mouse.x > 0 && mouse.x < root.width) && (mouse.y > 0 && mouse.y < root.height)) {
                    var xOffset = mouse.x - xStart
                    var yOffset = mouse.y - yStart
                    root.originX = visuWindowXStart + xOffset
                    root.originY = visuWindowYStart + yOffset
                }
            } else { // To map the tmpVisuWindow (zoom)
                root.originX = visuWindow.x
                root.originY = visuWindow.y
                tmpVisuWindow.width = visuWindow.width
                tmpVisuWindow.height = visuWindow.height
            }*/
        }
    }

    Graph {
        id: graphMiniature
        readOnly: true
        miniatureState: true
        anchors.fill: parent
        color: "transparent"
        x: (parent.marginLeft * 0.5) * parent.scaleFactor
        y: (parent.marginTop * 0.5) * parent.scaleFactor
        opacity: 1

        Rectangle {
            id: visuWindow
            border.color: "white"
            border.width: 1
            color: "transparent"
            width: 50
            height: 50
        }
    }
}

import QtQuick 1.1
import Canvas 1.0

Item {
    id: connectionItem
    property variant connectionModel
    property int x1
    property int y1
    property int x2
    property int y2

    Canvas {
        id: connection

        QtObject {
            id: m
            property variant connectionModel: connectionItem.connectionModel
        }

        property int canvasMargin: 20
        property int inPath: 0
        property int r: 0
        property int g: 178
        property int b: 161

        width: Math.abs(x1 - x2) + 2*canvasMargin
        height: Math.abs(y1 - y2) + 2*canvasMargin
        x: Math.min(x1, x2) - canvasMargin
        y: Math.min(y1, y2) - canvasMargin
        color: "transparent"
        state: "normal"

        StateGroup{
            id: stateConnection
            states: [
                State {
                    name: "selectedConnection"
                    when: m.connectionModel == _buttleData.currentConnectionWrapper
                    PropertyChanges { target: connection; r: 187; g: 187; b: 187 }
                },
                State {
                    name: "normal"
                    when: m.connectionModel != _buttleData.currentConnectionWrapper
                    PropertyChanges { target: connection; r: 0; g: 178; b: 161 }
                }
            ]
            // Need to re-paint the connection after each change of state.
            onStateChanged: {
                connection.requestPaint()
            }
        }

        // Drawing a curve for the connection
        onPaint: {
            var ctx = getContext();
            var cHeight = height;
            var cWidth = width;
            var startX = 0
            var startY = 0
            var endX = 0
            var endY = 0
            var controlPointXOffset = 40;
            ctx.strokeStyle = "rgb("+r+", "+g+", "+b+")";
            ctx.lineWidth = 2;

            ctx.beginPath()

            if(x1 <= x2
            && y1 <= y2){
                startX = canvasMargin
                startY = canvasMargin
                endX = width - canvasMargin
                endY = height - canvasMargin
            }
            if(x1 <= x2
            && y1 > y2){
                startX = canvasMargin
                startY = height - canvasMargin
                endX = width - canvasMargin
                endY = canvasMargin
            }
            if(x1 > x2
            && y1 <= y2){
                startX = width - canvasMargin
                startY = canvasMargin
                endX = canvasMargin
                endY = height - canvasMargin
            }
            if(x1 > x2
            && y1 > y2){
                startX = width - canvasMargin
                startY = height - canvasMargin
                endX = canvasMargin
                endY = canvasMargin
            }

            ctx.moveTo(startX , startY)
            ctx.bezierCurveTo(startX + controlPointXOffset, startY, endX - controlPointXOffset, endY, endX, endY)
            ctx.stroke()
            ctx.closePath()
        }

        MouseArea {
            // Returns true if we click on the curve
            function intersectPath(mouseX, mouseY, margin){
                for(var x = mouseX - margin; x< mouseX + margin; x++){
                    for(var y = mouseY - margin; y< mouseY + margin; y++){
                        if(connection.getContext().isPointInPath(x, y)){
                            return true;
                        }
                    }
                }
                return false;
            }

            anchors.fill: parent
            hoverEnabled: true

            //Propagate the event to the connections below
            onPressed: mouse.accepted = intersectPath(mouseX, mouseY, 5)
            onClicked: _buttleData.currentConnectionWrapper = m.connectionModel
            // The accepted property of the MouseEvent parameter is ignored in this handler.
            onPositionChanged: {
                mouse.accepted = intersectPath(mouseX, mouseY, 5)
            }
        }
    }
}

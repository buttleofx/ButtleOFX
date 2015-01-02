import QtQuick 2.0

Canvas {
    property int x1
    property int y1
    property int x2
    property int y2

    property bool readOnly
    property bool miniatureState  // TODO: named stated displayState

    property int canvasMargin: 20
    property int inPath: 0
    property int r: 0
    property int g: 178
    property int b: 161

    width: Math.abs(x1 - x2) + 2* canvasMargin
    height: Math.abs(y1 - y2) + 2* canvasMargin
    x: Math.min(x1, x2) - canvasMargin
    y: Math.min(y1, y2) - canvasMargin
    // color: "transparent"

    // Drawing a curve for the connection
    onPaint: {
        var ctx = getContext("2d")
        var cHeight = height
        var cWidth = width
        var startX = 0
        var startY = 0
        var endX = 0
        var endY = 0
        var controlPointXOffset = 40 * zoomCoeff
        ctx.strokeStyle = "rgb(" + r + ", " + g + ", " + b + ")"
        ctx.lineWidth = 2

        ctx.beginPath()

        if (x1 <= x2 && y1 <= y2) {
            startX = canvasMargin
            startY = canvasMargin
            endX = width - canvasMargin
            endY = height - canvasMargin
        }
        if (x1 <= x2 && y1 > y2) {
            startX = canvasMargin
            startY = height - canvasMargin
            endX = width - canvasMargin
            endY = canvasMargin
        }
        if (x1 > x2 && y1 <= y2) {
            startX = width - canvasMargin
            startY = canvasMargin
            endX = canvasMargin
            endY = height - canvasMargin
        }
        if (x1 > x2 && y1 > y2) {
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
}

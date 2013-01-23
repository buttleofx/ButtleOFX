import QtQuick 1.1

// grid of squares to see the transparency
Grid {
    id: gridOfSquares

    property int cellSize: 5

    anchors.fill: parent
    rows: height/cellSize
    columns: width/cellSize
    clip: true
    Repeater {
        model: gridOfSquares.columns*gridOfSquares.rows
        Rectangle {
            width: gridOfSquares.cellSize; height: gridOfSquares.cellSize
            color: (index%2 == 1) ? "grey" : "white"
        }
    }
}

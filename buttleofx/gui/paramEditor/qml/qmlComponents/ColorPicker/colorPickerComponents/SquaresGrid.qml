import QtQuick 1.

Grid {
    id: gridOfSquares
    property int cellSide: 10
    width: 110; height: 110
    rows: height/cellSide; columns: width/cellSide
    Repeater {
        model: gridOfSquares.columns*gridOfSquares.rows
        Rectangle {
            width: gridOfSquares.cellSide; height: gridOfSquares.cellSide
            color: (index%2 == 0) ? "gray" : "white"
        }
    }
}
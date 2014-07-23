import QtQuick 2.0

Grid {
    id: gridOfSquares
    width: 110
    height: 110
    rows: height / cellSide
    columns: width / cellSide
    property int cellSide: 10

    Repeater {
        model: gridOfSquares.columns * gridOfSquares.rows

        Rectangle {
            width: gridOfSquares.cellSide
            height: gridOfSquares.cellSide
            color: (index%2 == 0) ? "gray" : "white"
        }
    }
}

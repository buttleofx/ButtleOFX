import QtQuick 2.2
import QtQuick.Layouts 1.1

GridLayout {
    id: root

    columnSpacing: 0
    rowSpacing: 0
    rows: 8
    columns: 11

    Repeater {
        model: root.columns*root.rows
        Rectangle {
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.maximumHeight: 10
            color: (index%2 == 0) ? "gray" : "white"
        }
    }
}

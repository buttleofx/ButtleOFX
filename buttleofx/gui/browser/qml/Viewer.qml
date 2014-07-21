import QtQuick 2.0

Rectangle {
    id: viewer
    color: "red"
    property string filepath

    Image {
        x: 25
        source: viewer.filepath
        sourceSize.width: parent.width - 20
        sourceSize.height: parent.height - 20
    }
}

import QtQuick 2.0
import QtQuick.Layouts 1.1
import "../." // Qt-BUG import qmldir to use config singleton

Rectangle {
    id: root
    property vector4d colorRGBA

    border.width: Config.borderWidth
    border.color: Config.borderColor
    radius: Config.radius
    color: Config.backgroundColor

    RowLayout {
        anchors.fill: parent
        anchors.margins: Config.borderWidth
        spacing: 0

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: Qt.rgba(root.colorRGBA.x, root.colorRGBA.y,
                           root.colorRGBA.z, 1)
        }

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true

            Image {
                anchors.fill: parent
                source: "../img/checkerboard.jpg"
                fillMode: Image.Tile
            }

            Rectangle {
                anchors.fill: parent
                color: Qt.rgba(root.colorRGBA.x, root.colorRGBA.y,
                               root.colorRGBA.z, root.colorRGBA.w)
            }
        }
    }
}

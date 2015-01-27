import QtQuick 2.0
import QtQuick.Controls 1.1
import "../../qml/QuickMamba/." // Qt-BUG import qmldir
import QtQuick.Layouts 1.1

Rectangle
{
    id: root
    color: "black"
    width: 300
    height: 250

    RowLayout {
        anchors.centerIn: parent
        spacing: 20

        ScreenPicker {
            id:screenPicker

            onGrabbedColor: colorPreview.color = color
        }

        Rectangle {
            id:colorPreview
            color:"#00b2a1"

            radius: 3
            Layout.minimumWidth: 80
            Layout.minimumHeight: 80
        }
    }
}

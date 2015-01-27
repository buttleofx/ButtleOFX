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

            onGrabbedColor: {colorPreview.color = color; console.debug(color) ; }
        }

        Rectangle {
            id:colorPreview
            color:"white"
            radius: 3
            Layout.minimumWidth: 80
            Layout.minimumHeight: 80
        }
    }
}

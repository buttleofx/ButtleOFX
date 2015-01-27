import QtQuick 2.0
import QuickMamba 1.0

Rectangle
{
    id:root
    property string pickerImg: "assets/img/screenpicker/screenPicker.png"
    property string pickerImgHover: "assets/img/screenpicker/screenPickerHover.png"
    // Default style
    color: "#212121"
    border.width: 2
    border.color: "#333"
    radius: 3
    height: pickerImg.height * 2
    width: pickerImg.width * 2

    signal accepted
    signal grabbedColor(var color)

    Image {
        id: pickerImg
        source: root.pickerImg
        anchors.centerIn: parent
    }

    MouseArea {
        anchors.fill: root
        hoverEnabled: true

        onEntered: pickerImg.source = root.pickerImgHover
        onExited: pickerImg.source = root.pickerImg

        onPressed: screenPicker.grabbing = true
    }

    ColorPicker {
        id: screenPicker

        onAccepted: root.accepted()
        onCurrentColorChanged: root.grabbedColor(currentColor)
    }
}

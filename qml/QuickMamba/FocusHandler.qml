import QtQuick 2.0

MouseArea {
    anchors.fill: parent
    onClicked: {
        parent.forceActiveFocus()
    }
}

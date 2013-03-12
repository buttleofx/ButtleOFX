import QtQuick 1.1

MouseArea {
    anchors.fill: parent
    onClicked: {
        parent.forceActiveFocus()
    }
}

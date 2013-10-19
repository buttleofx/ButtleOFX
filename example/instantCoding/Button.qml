import QtQuick 2.0
 
Item {
    id: container

    property alias text: m.text
    property alias textColor: m.textColor
    signal clicked()
    width: 100
    height: 200

    QtObject {
        // Internal properties manager
        id: m

        property string text
        property color textColor
    }

    Text {
        id: buttonText
        
        text: m.text
        color: m.textColor
        width: paintedWidth + 10
        height: paintedHeight + 10
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter

        Rectangle {
            id: background

            anchors {
                fill: parent
                centerIn: parent
            }
            color: "red"
            z: -1

            MouseArea {
                anchors.fill: parent
                onClicked: container.clicked()
            }
        }
    }
}
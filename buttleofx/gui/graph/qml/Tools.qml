import QtQuick 1.1

Rectangle {
    id: tools
    width: 850
    height: 30

    signal clickCreationNode(string nodeType)

    z: 2000
    anchors.top: parent.top
    color: "#212121"

    Rectangle {
        id: addNodeButton
        implicitWidth: 20
        implicitHeight: 20
        width: 7/10 * parent.height
        height: width
        anchors.verticalCenter: parent.verticalCenter
        color: "#212121"
        Text {
            anchors.centerIn: parent
            text: "+"
            font.pointSize: 16
            color: "white"
        }
        MouseArea {
            anchors.fill: parent
            onClicked: {
                listmodel.clickFrom = tools
                listmodel.menuState = (listmodel.menuState == "hidden") ? "shown" : "hidden"
            }
        }
    }

    Rectangle {
        id: delNodeButton
        implicitWidth: 20
        implicitHeight: 20
        width: 7/10 * parent.height
        height: width
        x: 30
        y: 6
        color: "#212121"
        Text {
            anchors.centerIn: parent
            text: "-"
            font.pointSize: 16
            color: "white"
        }
        MouseArea {
            anchors.fill: parent
            onClicked: {
                _buttleData.destructionNode()
            }
        }
    }

//    MenuList {
//        id: listmodel
//    }
}

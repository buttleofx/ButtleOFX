import QtQuick 1.1

Rectangle {
    id: nodeMenuElement
    width: 120
    height: 20
    color: "#343434"

    property string labelElement
    property string parentName
    property variant children: null
    property string tuttleId: 'tuttle.' + labelElement
    property variant type: _buttleData.isAPlugin(tuttleId) ? "node" : "category"
    property variant clickFrom: tools

    Text {
        anchors.left: parent.left
        anchors.leftMargin: 15
        anchors.verticalCenter: parent.verticalCenter
        color: "#eee"
        text: nodeMenuElement.labelElement
    }
    MouseArea {
        anchors.fill: parent
        hoverEnabled: true

        onExited: {
            parent.color = "#343434"
            if (mouseX <= nodeMenuElement.x + nodeMenuElement.width - 10) {
                if (nodeMenuElement.children) {
                    nodeMenuElement.children.destroy();
                }
            }
        }
        onEntered: {
            parent.color = "#bbb"
            if(type=="category"){
                if (nodeMenuElement.children) {
                    nodeMenuElement.children.destroy();
                }

                var newComponent = Qt.createQmlObject('MenuList { parentName: "' + nodeMenuElement.parentName + nodeMenuElement.labelElement + '/"; x: ' + parent.width + '; }', parent);
                nodeMenuElement.children = newComponent
            }
        }

        onClicked: {
            if (nodeMenuElement.type == "node") {
                clickFrom.clickCreationNode(nodeMenuElement.tuttleId)
            }
        }
    }
}

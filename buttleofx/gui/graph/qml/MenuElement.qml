import QtQuick 1.1

Rectangle {
    id: nodeMenuElement
    width: 120
    height: 20
    color: "#343434"

    property string labelElement
    property string parentName

    // if the submenu of this element is open (= if "MenuElement has children"), property children is this submenu just created. Else, null.
    property variant children: null

    //property string tuttleId: 'tuttle.' + labelElement
    property string tuttleId: labelElement
    property variant type: _buttleData.isAPlugin(tuttleId) ? "plugin" : "category"
    property variant clickFrom: tools

    Text {
        anchors.left: parent.left
        anchors.leftMargin: 15
        anchors.verticalCenter: parent.verticalCenter
        color: type == "category" ? "#eee" : "black"
        text: nodeMenuElement.labelElement
    }
    MouseArea {
        anchors.fill: parent
        hoverEnabled: true

        // On mouse exited the element, we destroy its children if it exists.
        onExited: {
            parent.color = "#343434"
            if (mouseX <= nodeMenuElement.x + nodeMenuElement.width - 10) {
                if (nodeMenuElement.children) {
                    nodeMenuElement.children.destroy();
                }
            }
        }

        // On mouse entered the element, we create the new MenuList of its children (only if this element is a category)
        onEntered: {
            parent.color = "#bbb"
            if(type=="category") {
                if (nodeMenuElement.children) {
                    nodeMenuElement.children.destroy();
                }

                var newComponent = Qt.createQmlObject('MenuList { parentName: "' + nodeMenuElement.parentName + nodeMenuElement.labelElement + '/"; x: ' + parent.width + '; }', parent);
                nodeMenuElement.children = newComponent
            }
        }

        // On mouse clicked, we call the creationNode fonction if the element is a plugin.
        onClicked: {
            if (nodeMenuElement.type == "plugin") {
                clickFrom.clickCreationNode(nodeMenuElement.tuttleId)
            }
        }
    }
}

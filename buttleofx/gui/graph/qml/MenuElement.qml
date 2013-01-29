import QtQuick 1.1

Rectangle {
    width: 160
    height: 20
    color: "#343434"

    property string labelElement
    property string idElement
    property string parentName

    property variant menuListItem
    // if the submenu of this element is open (= if "MenuElement has children"), property children is this submenu just created. Else, null.
    property variant children: null

    property variant type: _buttleData.isAPlugin(idElement) ? "plugin" : "category"
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
            nodeMenuElement.color = "#343434"
            if (mouseX <= nodeMenuElement.x + nodeMenuElement.width - 10) {
                menuListItem.destroyNextMenu();
            }
        }

        // On mouse entered the element, we create the new MenuList of its children (only if this element is a category)
        onEntered: {
            nodeMenuElement.color = "#bbb"
            if(type=="category") {
                menuListItem.destroyNextMenu();
                menuListItem.createNextMenu(nodeMenuElement.parentName, nodeMenuElement.labelElement, nodeMenuElement.x + nodeMenuElement.width, nodeMenuElement.y)
            }
        }

        // On mouse clicked, we call the creationNode fonction if the element is a plugin. Then we destroy the menu.
        onClicked: {
            if (nodeMenuElement.type == "plugin") {
                console.log("creation node")
                clickFrom.clickCreationNode(nodeMenuElement.idElement);
                if (tools.children) {
                    tools.children.destroy();
                }
            }
        }
    }
}

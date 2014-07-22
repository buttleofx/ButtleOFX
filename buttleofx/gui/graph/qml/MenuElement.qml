import QtQuick 2.0

Rectangle {
    property string labelElement
    property string idElement
    property string parentName

    // The MenuList where the element comes from
    property variant menuListItem

    // To remember the path
    color: menuListItem.currentElementLabel == labelElement ? "#bbb" : "#343434"

    property variant type: _buttleData.isAPlugin(idElement) ? "plugin" : "category"
    property variant clickFrom: tools

    Text {
        id: textMenuElement
        anchors.left: parent.left
        anchors.leftMargin: 15
        anchors.verticalCenter: parent.verticalCenter
        color: type == "category" ? "#eee" : "#00b2a1"
        text: nodeMenuElement.labelElement
    }

    MouseArea {
        anchors.fill: parent
        hoverEnabled: true

        // On mouse exited the element, we destroy its submenu if it exists.
        onExited: {
            // Menu rolls out on the right
            if ((mouseX <= nodeMenuElement.x + nodeMenuElement.width - 10) && (menulist.side == "right")) {
                //menuListItem.destroyNextMenu();
            }
            // Menu rolls out on the left
            if ((mouseX >= nodeMenuElement.x + 10) && (menulist.side == "left")) {
                //menuListItem.destroyNextMenu();
            }
        }

        // On mouse entered the element, we create the new next menu (only if this element is a category)
        onEntered: {
            menuListItem.currentElementLabel = textMenuElement.text

            if (type=="category") {
                menuListItem.destroyNextMenu();
                // Menu rolls out on the right
                if (menulist.side == "right") {
                    menuListItem.createNextMenu(nodeMenuElement.parentName, nodeMenuElement.labelElement, nodeMenuElement.x + nodeMenuElement.width, nodeMenuElement.y, nodeMenuElement.clickFrom, "right");
                } else if (menulist.side == "left") { // Menu rolls out on the left
                    menuListItem.createNextMenu(nodeMenuElement.parentName, nodeMenuElement.labelElement, nodeMenuElement.x, nodeMenuElement.y, nodeMenuElement.clickFrom, "left");
                    // menuListItem.nextMenu.x = menuListItem.nextMenu.x - menulist.width
                }

            }
        }

        // On mouse clicked, we call the creationNode fonction if the element is a plugin. Then we destroy the menu.
        onClicked: {
            if (nodeMenuElement.type == "plugin") {
                clickFrom.clickCreationNode(nodeMenuElement.idElement);
                if (tools.menuComponent) {
                    tools.menuComponent.destroy();
                }
            }
        }
    }
}

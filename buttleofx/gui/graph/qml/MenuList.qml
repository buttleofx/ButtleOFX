import QtQuick 1.1

Item {
    id: menulist

    // parentName = the key for the python dictionary of plugins. Ex: 'tuttle/image/' or 'tuttle/image/process/filter/
    property string parentName
    property variant clickFrom: graph
    property int heightElement: 22
    property int widthElement: 160

    ListView {
        width: 160
        id: nodeMenuView
        model: _buttleData.getQObjectPluginsIdentifiersByParentPath(menulist.parentName)
        height: heightElement * model.count
        property variant nextMenu: null
        property variant currentElementLabel: ""

        function destroyNextMenu()
        {
            if( nodeMenuView.nextMenu )
                nodeMenuView.nextMenu.destroy()
        }

        function createNextMenu(parentName, labelElement, x, y, clickFromB)
        {
            destroyNextMenu()
            print("CreateNextMenu", clickFrom);
            var newComponent = Qt.createQmlObject('MenuList { parentName: "' + parentName + labelElement + '/"; x: ' + x + '; y: ' + y +  '; clickFrom: ' + String(clickFromB) + '; }', nodeMenuView);
            print("New  CreatedComponent : ", newComponent.clickFrom)
            nodeMenuView.nextMenu = newComponent
        }

        delegate {
            Component {
                MenuElement {
                    id: nodeMenuElement
                    labelElement: object[0]
                    idElement: object[1]
                    parentName: menulist.parentName
                    menuListItem: nodeMenuView
                    height: heightElement
                    width: widthElement
                    property variant clickFrom: menulist.clickFrom
                }
            }
        }
    }

}

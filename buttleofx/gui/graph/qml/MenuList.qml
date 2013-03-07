import QtQuick 1.1

Item {
    id: menulist

    // ParentName = the key for the python dictionary of plugins. Ex: 'tuttle/image/' or 'tuttle/image/process/filter/
    property string parentName
    property variant clickFrom: tools
    property int heightElement: 22
    //property int widthElement: 160
    property int max: 0
    property string side: "right"
    z: 1000

    ListView {
        width: 160
        id: nodeMenuView
        model: _buttleData.getQObjectPluginsIdentifiersByParentPath(menulist.parentName)
        height: heightElement * model.count
        property variant nextMenu: null
        property variant currentElementLabel: ""

        // Destroy the next menu if it exists
        function destroyNextMenu() {
            if( nodeMenuView.nextMenu ) {
                nodeMenuView.nextMenu.destroy()   
            }
                
        }

        // Create a next menu
        function createNextMenu(parentName, labelElement, x, y, clickFrom) {
            destroyNextMenu()
            var newComponent = Qt.createQmlObject('MenuList { parentName: "' + parentName + labelElement + '/"; x: ' + x + '; y: ' + y +  ';}', nodeMenuView);
            newComponent.clickFrom = clickFrom;
            newComponent.side = menulist.side;
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
                    width: menulist.max * 8 + 30
                    property int max: maxElement(nodeMenuElement)
                    property variant clickFrom: menulist.clickFrom

                    // Calculates the length of the longest label in the menuElement
                    function maxElement(nodeMenuElement) {
                        if(menulist.max < nodeMenuElement.labelElement.length) {
                            menulist.max = nodeMenuElement.labelElement.length;
                        }
                        return menulist.max
                    }

                }
            }
        }
    }
}

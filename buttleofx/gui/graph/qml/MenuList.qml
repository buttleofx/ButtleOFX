import QtQuick 1.1

Item {
    id: menulist

    // parentName = the key for the python dictionary of plugins. Ex: 'tuttle/image/' or 'tuttle/image/process/filter/
    property string parentName
    property variant clickFrom: tools

    ListView {
        height: 300
        id: nodeMenuView
        model: _buttleData.getQObjectPluginsIdentifiersByParentPath(menulist.parentName)
        delegate {
            Component {
                MenuElement {
                    labelElement: object
                    parentName: menulist.parentName
                }
            }
        }
    }

}

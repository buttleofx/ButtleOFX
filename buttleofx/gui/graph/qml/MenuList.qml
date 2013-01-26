import QtQuick 1.1

Item {
    id: menulist
    property string parentName
    property variant clickFrom: tools

    ListView {
        //property variant children: null
        height: 5000 // à changer
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



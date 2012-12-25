//import Qt 4.7
import QtQuick 1.1

Rectangle {
    id: paramEditor
    //parent of the ParamEditor is the Row of the ButtleAp
    //width is 30% of the row
    //width: 30/100 * parent.width
    //height: parent.height

    implicitWidth: 300
    implicitHeight: 500

    color: "#212121"

    ListView {
        id: paramElementList
        anchors.fill: parent
        model: _paramListModel.paramElmts

        delegate: Component {
            Loader {
                id: param
                source : model.object.paramType + ".qml"
                height: 50
            }
        }
    }
}

/*
Rectangle {
    width: parent.width
    height: 40
    color: ((index % 2 === 0)?"#222":"#111")
    
    Loader {
        id: param
       source: ((index % 2 === 0)? "ParamInt.qml":"ParamString.qml")
    }*/

    /*
    Text {
        text: model.object.defaultValue
        anchors {
            left: parent.left; leftMargin: 10
            verticalCenter: parent.verticalCenter
        }
        color: "white"
        font.bold: true
        elide: Text.ElideRight
    }
}*/


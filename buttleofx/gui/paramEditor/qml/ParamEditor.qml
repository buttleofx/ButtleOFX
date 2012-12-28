//import Qt 4.7
import QtQuick 1.1

Rectangle {
    id: paramEditor
    //parent of the ParamEditor is the Row of the ButtleAp
    //width is 30% of the row
    //width: 30/100 * parent.width
    //height: parent.height

    width: 300
    height: 500

    gradient: Gradient {
        GradientStop { position: 0.05; color: "#111111" }
        GradientStop { position: 0.1; color: "#141414" }
    }

    Rectangle{
        id:mainMenu
        width: parent.width
        height: 30
        color: "#141414"

        Text {
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            anchors.leftMargin: 10
            color: "white"
            text: "Parameters"
            font.pointSize: 11
        }
    }

    ListView {
        id: paramElementList
        anchors.fill: parent
        anchors.margins: 20
        anchors.topMargin: 50
        model: _paramListModel.paramElmts

        delegate: Component {
            Loader {
                id: param
                source : model.object.paramType + ".qml"
                height: 30
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


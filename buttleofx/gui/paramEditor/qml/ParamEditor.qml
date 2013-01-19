import QtQuick 1.1
import QtDesktop 0.1

//parent of the ParamEditor is the Row of the ButtleAp
Rectangle {
    id: paramEditor

    property variant params 

    implicitWidth: 300
    implicitHeight: 500

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
        model: params

        delegate: Component {
            Loader {
                id: param
                source : model.object.paramType + ".qml"
                height: 30
                width: parent.width
            }
        }
    }

    Slider{

    y:30

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


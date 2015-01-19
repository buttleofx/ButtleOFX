import QtQuick 2.0
import BrowserModel 1.0

Rectangle {

    width: 800
    height: 600
    color: "red"

    MouseArea {
        anchors.fill: parent

        onClicked: {
            console.log("hello")
        }
    }

    Rectangle {
        width: 100
        height: 100
        color: "blue"

        MouseArea {
            anchors.fill: parent

            onClicked: {
                console.log("hello")
            }
        }
    }

    BrowserModel {
        id: browser
    }

    Text {
         id: helloText
         text: "Coucou"
     }


}

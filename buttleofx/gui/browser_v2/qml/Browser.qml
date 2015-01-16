import QtQuick 2.0
import Browser 1.0

Rectangle {

    width: 800
    height: 600
    color: "red"

    MouseArea {
        anchors.fill: parent

        onClicked: {
            console.log("hello")
            browser.title = "hellllooooo"
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
                browser.greeting()
            }
        }
    }

    Browser {
        id: browser
        title: "Plopinette"
    }

    Text {
         id: helloText
         text: browser.title
     }


}

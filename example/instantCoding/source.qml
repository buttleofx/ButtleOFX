import QtQuick 1.1
 
Item {
    width: 300
    height: 200

    Button {
        id: myButton

        text: "Click me !"
        textColor: "black"
        onClicked: console.log("Clicked !")
    }
}

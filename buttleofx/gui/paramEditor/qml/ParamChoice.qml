import QtQuick 1.1
import QtDesktop 0.1

Item {
    id: choiceList
    implicitWidth: 300
    implicitHeight: 30
    property alias title: paramChoiceTitle.text
    property variant paramObject: model.object

    Row {
        id: paramChoiceInputContainer
        spacing: 10

        //Title of the param
        Text {
            id: paramChoiceTitle
            width: 80
            text: paramObject.text + " : "
            color: "white"
            anchors.top: parent.top
            anchors.verticalCenter: parent.verticalCenter
        }

        // Container of the diplay
        Item {
            id: container
            width: 40
            height: 20

            // First Item = item chosen
            Rectangle {
                id: firstElement
                width: 120
                height: 20
                color: "#212121"
                border.width: 1
                        border.color: "#333"
                radius: 3

                Text{
                    id: intitule
                    anchors.left: parent.left
                    anchors.leftMargin: 5
                    anchors.verticalCenter: parent.verticalCenter
                    text: paramObject.value
                    color: "white"

                }
        
                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    onClicked: {         
                        elements.state = ( elements.state == "hidden") ? "shown" : "hidden"
                    }
                }
            }

        
            // All the items available
            Rectangle {
                id: elements
                height: 20
                width: 40
                state: "hidden"
                x: firstElement.x
                y: firstElement.y

                Repeater {
                    id: repeater
                    model: paramObject.listValue

                    Rectangle {
                        id: itemElement
                        width: 120
                        height: 20
                        anchors.left: parent.left
                        y: parent.y + 20*index 
                        color: "#343434"
                        border.width: 1
                        border.color: "#333"
                        Text{
                            id: textElement
                            anchors.left: parent.left
                            anchors.leftMargin: 10
                            anchors.verticalCenter: parent.verticalCenter
                            text: model.object
                            color: "white"

                        }
                        
                        MouseArea {
                            anchors.fill: parent
                            hoverEnabled: true
                            onEntered: parent.color = "#bbb"
                            onExited: parent.color = "#343434"
                            onClicked: {             
                                elements.state = "hidden"
                                paramObject.value = textElement.text

                            }
                        }
                    }
                    
                }

                states: [
                    State {
                        name: "hidden"
                        PropertyChanges {
                            target: elements
                            opacity: 0
                        }
                    },
                    State {
                        name: "shown"
                        PropertyChanges {
                            target: elements
                            opacity: 1
                        }
                    }
                ]  
            }
        }
       
    }
}






// List
       /*Item {
            height: 20
            width: 40


            ComboBox {
                //model: paramObject.listValue
                width: 150
                height: 20
                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter

                MenuItem {
                    text: "POIU"
                }
                MenuItem {
                    text: "ihiihihih"
                }
                MenuItem {
                    text: "POIU"
                }
                MenuItem {
                    text: "POIU"
                }
                
                Repeater {
                    id: ohoh
                    model: 5
                }
            } 
        }*/






        /*ListModel {
            id: nodeMenuModel

            ListElement { cat2: "Invert" }
            ListElement { cat2: "Gamma" }
            ListElement { cat2: "Blur" }
            ListElement { cat2: "Crop" }
            ListElement { cat2: "Resize" }
        }

        ListView {
            id: nodeMenuView
            x: 0
            y: 30
            width: 120
            height: 500
            model: nodeMenuModel
            delegate {
                Rectangle {
                    width: 120
                    height: 20
                    color: "#343434"
                    Text {
                        anchors.left: parent.left
                        anchors.leftMargin: 15
                        anchors.verticalCenter: parent.verticalCenter
                        color: "#eee"
                        text: cat2
                    }
                    MouseArea {
                        anchors.fill: parent
                        hoverEnabled: true
                        onEntered: parent.color = "#bbb"
                        onExited: parent.color = "#343434"
                        onClicked: {
                            console.log(cat2)
                            mainElement.text = cat2
                        }
                    }
                }
            }
        } */

/*
    function fillModel() {
        for(element in model.object.listValue) {
            commonModel.append( "ListElement{text: \"element\"}" );
            console.log("Element")
        }
    }*/


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
            text: paramObject.text + " : "
            color: "white"
        }

        // Container of the diplay
        Item {
            id: container
            width: 40
            height: 20

            // Current value
            Row{
            spacing: 2
                Rectangle {
                    id: firstElement
                    width: intitule.width + 10
                    height: 20
                    color: "#343434"
                    border.width: 1
                    border.color: "#444"
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
                Rectangle {
                    width: 20
                    height: 20
                    color: "#343434"
                    border.width: 1
                    border.color: "#444"
                    Image {
                        id: arrow
                        source: "img/arrow.png"
                        anchors.centerIn: parent
                    }
                    MouseArea {
                        anchors.fill: parent
                        hoverEnabled: true
                        onClicked: {         
                            elements.state = ( elements.state == "hidden") ? "shown" : "hidden"
                        }
                    }
                }
            }


        
            // List of the values
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
                        width: textElement.width + 10
                        height: 20
                        anchors.left: parent.left
                        y: parent.y + 20*index
                        color: "#343434"
                        border.width: 1
                        border.color: "#444"

                        Text{
                            id: textElement
                            anchors.left: parent.left
                            anchors.leftMargin: 5
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
                                paramObject.value = model.object 
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

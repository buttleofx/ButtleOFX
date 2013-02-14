import QtQuick 1.1
import QtDesktop 0.1

Item {
    id: choiceList
    implicitWidth: 300
    implicitHeight: 30
    property alias title: paramChoiceTitle.text
    property variant paramObject: model.object
    //z: 1


    // convert the qobjectlistmodel into a qml ListModel
    ListModel {
        id: menuItems
    }
    Component.onCompleted: {
        for( var i=0; i < paramObject.listValue.count; i++ )
        {
            menuItems.append( {"text": paramObject.listValue.get(i)} )
        }
    }

    Row {
        id: paramChoiceInputContainer
        spacing: 10

        //Title of the param
        Text {
            id: paramChoiceTitle
            text: paramObject.text + " : "
            color: "white"
        }

        ComboBox {
            model: menuItems
            //width: 100
            height: 20
            onSelectedIndexChanged: console.debug("-> " + menuItems.get(selectedIndex).text + ", " + paramObject.listValue.get(selectedIndex))
        }
    
        //

        // Container of the diplay
        Item {
            id: container
            width: 40
            height: 20

            // Current value
            Row {
                spacing: 2
                Rectangle {
                    id: firstElement
                    //width: intitule.width + 10
                    width: repeater.maxWidth
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
                            container.forceActiveFocus()
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
                            container.forceActiveFocus()
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
                //z: firstElement.z + 10

                Repeater {
                    id: repeater
                    //z: 20

                    model: paramObject.listValue

                    property int maxWidth: 0

                    Rectangle {
                        id: itemElement
                        width: repeater.maxWidth
                        height: 20
                        anchors.left: parent.left
                        //y: parent.y + 20*index
                        y: - parent.y - 20*index // we temporary display the list on the top of the current value : no problem of superposition...
                        color: "#343434"
                        border.width: 1
                        border.color: "#444"
                        //z: elements.z + 1000

                        Text{
                            id: textElement
                            anchors.left: parent.left
                            anchors.leftMargin: 5
                            anchors.verticalCenter: parent.verticalCenter
                            text: model.object
                            color: "white"

                            onWidthChanged: {
                                if (repeater.maxWidth < textElement.width) {
                                    repeater.maxWidth = textElement.width + 10
                                }
                            }
                        }
                        
                        MouseArea {
                            anchors.fill: parent
                            hoverEnabled: true
                            onEntered: parent.color = "#bbb"
                            onExited: parent.color = "#343434"
                            onClicked: {           
                                elements.state = "hidden"
                                paramObject.value = model.object 

                                //take the focus of MainWindow
                                container.forceActiveFocus()
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
        //
    }
}

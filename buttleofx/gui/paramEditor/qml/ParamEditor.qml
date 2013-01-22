import QtQuick 1.1
import QtDesktop 0.1

//parent of the ParamEditor is the Row of the ButtleAp
Rectangle {
    id: paramEditor

    property variant params 
    property variant current_node

    implicitWidth: 300
    implicitHeight: 500

    gradient: Gradient {
        GradientStop { position: 0.05; color: "#111111" }
        GradientStop { position: 0.1; color: "#141414" }
    }

    Rectangle{
        id: paramWidget
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
        id: tuttleParam

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

    Loader {
        sourceComponent: current_node ? nodeParam_component : undefined
        anchors.fill: parent
        Component {
            id: nodeParam_component
            Column{
                spacing: 10
                y: tuttleParam.y + tuttleParam.contentHeight

                Rectangle{
                    id: propertyWidget
                    width: paramEditor.width
                    height: 30
                    color: "#111111"

                    Text {
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.left: parent.left
                        anchors.leftMargin: 10
                        color: "white"
                        text: "Node properties"
                        font.pointSize: 11
                    }
                }

                Item{
                    id: nodeNameItem
                    implicitWidth: 300
                    implicitHeight: 30
                    anchors.left: parent.left
                    anchors.leftMargin: 10

                    /*Container of the textInput*/

                    Row{
                        id: nodeNameContainer
                        spacing: 10

                        /*Title of the paramInt */
                        Text {
                            id: nodeNameText
                            width: 80
                            text: "Name : "
                            color: "white"
                            anchors.top: parent.top
                            anchors.verticalCenter: parent.verticalCenter
                        }

                        /*Input field limited to 50 characters*/
                        Rectangle{
                            height: 20
                            implicitWidth: 200
                            color: "#212121"
                            border.width: 1
                            border.color: "#333"
                            radius: 3
                            TextInput{
                                id: nodeNameInput
                                text: current_node.name
                                anchors.left: parent.left
                                anchors.leftMargin: 5
                                maximumLength: 100
                                selectByMouse : true
                                color: activeFocus ? "white" : "grey"
                                onAccepted: current_node.name = nodeNameInput.text
                            }
                        }
                    }
                }
            
                Item{
                    id: nodeTypeItem
                    implicitWidth: 300
                    implicitHeight: 30
                    anchors.left: parent.left
                    anchors.leftMargin: 10

                    /*Container of the textInput*/

                    Row{
                        id: nodeTypeContainer
                        spacing: 10

                        /*Title of the paramInt */
                        Text {
                            id: nodeTypeText
                            width: 80
                            text: "Type : "
                            color: "white"
                            anchors.top: parent.top
                            anchors.verticalCenter: parent.verticalCenter
                        }

                        /*Input field limited to 50 characters*/
                        Rectangle{
                            height: 20
                            implicitWidth: 200
                            color: "transparent"
                            Text{
                                id: nodeTypeInput
                                text: current_node.nodeType
                                anchors.left: parent.left
                                anchors.leftMargin: 5
                                color: "white"
                            }
                        }
                    }
                }
            }
        }
    }
}


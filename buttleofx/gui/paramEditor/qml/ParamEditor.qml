import QtQuick 1.1
import QtDesktop 0.1

//parent of the ParamEditor is the Row of the ButtleAp
Rectangle {
    id: paramEditor

    property variant params 
    property variant current_node

    property color background: "#212121"
    property color backgroundInput: "#141414"
    property color gradian_1: background
    property color gradian_2: "#111111"
    property color borderInput: "#333"

    implicitWidth: 300
    implicitHeight: 500

    color: background

    Rectangle{
        id: paramEditorTittle
        width: parent.width
        height: 80
        color: paramEditor.background

        Text {
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.left: parent.left
            anchors.leftMargin: 10
            color: "white"
            font.weight: Font.DemiBold
            horizontalAlignment: Text.AlignHCenter
            font.pointSize: 15
            text: "Parameters"
        }

        gradient: Gradient {
            GradientStop { position: 0.65; color: paramEditor.gradian_1 }
            GradientStop { position: 1; color: paramEditor.gradian_2 }
        }
    }
    
    
    /* Tuttle for the parameters from Tuttle */
    Rectangle{
        id: tuttleParamTittle
        width: paramEditor.width
        height: 40
        color: paramEditor.background
        y: paramEditorTittle.height

        Text {
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            anchors.leftMargin: 10
            color: "white"
            font.underline: true
            font.pointSize: 12
            text: "Node properties from Tuttle"
        }

        gradient: Gradient {
            GradientStop { position: 0.95; color: paramEditor.gradian_1 }
            GradientStop { position: 1; color: paramEditor.gradian_2 }
        }
    }

    /* Params depend on the node type (Tuttle data)*/
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

    Rectangle{
        id: buttleParamTittle
        width: paramEditor.width
        height: 40
        color: paramEditor.background
        y: paramEditorTittle.height + tuttleParamTittle.height + tuttleParam.y + tuttleParam.contentHeight

        Text {
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            anchors.leftMargin: 10
            color: "white"
            font.underline: true
            font.pointSize: 12
            text: "Node properties from Buttle"
        }

        gradient: Gradient {
            GradientStop { position: 0.95; color: paramEditor.gradian_1 }
            GradientStop { position: 1; color: paramEditor.gradian_2 }
        }
    }

    Loader {
        sourceComponent: current_node ? nodeParam_component : undefined
        anchors.fill: parent
        anchors.topMargin: 10
        Component {
            id: nodeParam_component
            Column{
                spacing: 10
                y: buttleParamTittle.height + paramEditorTittle.height + tuttleParamTittle.height + tuttleParam.y + tuttleParam.contentHeight

                /*Name of the node (Buttle data)*/
                Item{
                    id: nodeNameItem
                    implicitWidth: 300
                    implicitHeight: 30
                    anchors.left: parent.left
                    anchors.leftMargin: 10

                    Row{
                        id: nodeNameContainer
                        spacing: 10

                        /* Title */
                        Text {
                            id: nodeNameText
                            width: 80
                            anchors.top: parent.top
                            anchors.verticalCenter: parent.verticalCenter
                            color: "white"
                            text: "Name : "
                        }

                        /* Input field limited to 50 characters */
                        Rectangle{
                            height: 20
                            implicitWidth: 200
                            color: paramEditor.backgroundInput
                            border.width: 1
                            border.color: paramEditor.borderInput
                            radius: 3
                            TextInput{
                                id: nodeNameInput
                                text: current_node.name
                                anchors.left: parent.left
                                anchors.verticalCenter: parent.verticalCenter
                                anchors.leftMargin: 5
                                maximumLength: 100
                                selectByMouse : true
                                color: activeFocus ? "white" : "grey"
                                onAccepted: current_node.name = nodeNameInput.text
                            }
                        }
                    }
                }
            
                /* Type of the node (Buttle data) */
                Item{
                    id: nodeTypeItem
                    implicitWidth: 300
                    implicitHeight: 30
                    anchors.left: parent.left
                    anchors.leftMargin: 10

                    Row{
                        id: nodeTypeContainer
                        spacing: 10

                        /* Title */
                        Text {
                            id: nodeTypeText
                            width: 80
                            text: "Type : "
                            color: "white"
                            anchors.top: parent.top
                            anchors.verticalCenter: parent.verticalCenter
                        }

                        /* Input field limited to 50 characters */
                        Rectangle{
                            height: 20
                            implicitWidth: 200
                            color: "transparent"
                            Text{
                                id: nodeTypeInput
                                text: current_node.nodeType
                                anchors.left: parent.left
                                anchors.leftMargin: 5
                                color: "grey"
                            }
                        }
                    }
                }

                /* Coord of the node (Buttle data) */
                Item{
                    id: nodecoordItem
                    implicitWidth: 300
                    implicitHeight: 30
                    anchors.left: parent.left
                    anchors.leftMargin: 10

                    Row{
                        id: nodeCoordContainer
                        spacing: 10

                        /* Title */
                        Text {
                            id: nodeCoordText
                            width: 80
                            text: "Coord (x, y) : "
                            color: "white"
                            anchors.top: parent.top
                            anchors.verticalCenter: parent.verticalCenter
                        }

                        /* Input field limited : x */
                        Rectangle{
                            height: 20
                            implicitWidth: 20
                            color: "transparent"
                            Text{
                                id: nodeCoordX
                                text: current_node.coord.x
                                anchors.left: parent.left
                                anchors.leftMargin: 5
                                color: "grey"
                            }
                        }
                        /* Input field limited : separated */
                        Rectangle{
                            height: 20
                            implicitWidth: 5
                            color: "transparent"
                            Text{
                                id: coordSeparated
                                text: "/"
                                anchors.left: parent.left
                                anchors.leftMargin: 5
                                color: "white"
                            }
                        }
                        /* Input field limited : y */
                        Rectangle{
                            height: 20
                            implicitWidth: 20
                            color: "transparent"
                            Text{
                                id: nodeCoordY
                                text: current_node.coord.y
                                anchors.left: parent.left
                                anchors.leftMargin: 5
                                color: "grey"
                            }
                        }
                    }
                }

                /* Color of the node (Buttle data) */
                Item{
                    id: nodecolorItem
                    implicitWidth: 300
                    implicitHeight: 30
                    anchors.left: parent.left
                    anchors.leftMargin: 10

                    Row{
                        id: nodeColorContainer
                        spacing: 10

                        /* Title */
                        Text {
                            id: nodeColorText
                            width: 80
                            text: "Color (Hex) : "
                            color: "white"
                            anchors.top: parent.top
                            anchors.verticalCenter: parent.verticalCenter
                        }

                        /* Input field limited : rgb */
                        Rectangle{
                            height: 20
                            implicitWidth: 80
                            color: paramEditor.backgroundInput
                            border.width: 1
                            border.color: paramEditor.borderInput
                            radius: 3
                            TextInput{
                                id: nodeColorRGBInput
                                text: current_node.color
                                anchors.left: parent.left
                                anchors.verticalCenter: parent.verticalCenter
                                anchors.leftMargin: 5
                                maximumLength: 50
                                selectByMouse : true
                                color: activeFocus ? "white" : "grey"
                                onAccepted: current_node.color = nodeColorRGBInput.text
                            }
                        }
                    }
                }
            }
        }
    }
}

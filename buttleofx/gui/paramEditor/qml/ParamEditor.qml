import QtQuick 1.1
import QtDesktop 0.1

import "ScrollBar"

//parent of the ParamEditor is the Row of the ButtleAp
Rectangle {
    id: paramEditor

    property variant params 
    property variant currentParamNode

    property color background: "#212121"
    property color backgroundInput: "#141414"
    property color gradian1: background
    property color gradian2: "#111111"
    property color borderInput: "#333"

    property color textColor : "white"
    property color activeFocusOn : "white"
    property color activeFocusOff : "grey"

    implicitWidth: 300
    implicitHeight: 500

    color: "#353535" // used to have the same color for the splitterColumn separator
    /*TITLE OF THE PARAMEDITOR*/
    /*Rectangle{
        id: paramEditorTitle
        width: parent.width
        height: 40
        color: paramEditor.background

        Text {
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.left: parent.left
            anchors.leftMargin: 10
            color: textColor
            font.weight: Font.DemiBold
            horizontalAlignment: Text.AlignHCenter
            font.pointSize: 12
            text: "Parameters"
        }

        gradient: Gradient {
            GradientStop { position: 0.65; color: paramEditor.gradian1 }
            GradientStop { position: 1; color: paramEditor.gradian2 }
        }
    }*/


    SplitterColumn {
        width: parent.width
        height: parent.height
        handleWidth: 3

        /*TUTTLE PARAMS*/
        Rectangle{
            Splitter.minimumHeight: tuttleParamTitle.height

            id: tuttleParams
            height: 550
            width: parent.width
            color: paramEditor.background
            /* title of tuttle params */
            

            /* Params depend on the node type (Tuttle data)*/
            Rectangle{
                id: tuttleParamContent
                height: parent.height - tuttleParamTitle.height
                width: parent.width
                y: tuttleParamTitle.height
                color: paramEditor.background

                property string lastGroupParam : "No Group."

                ListView {
                    id: tuttleParam
                    anchors.fill: parent
                    anchors.topMargin: 5
                    anchors.bottomMargin: 5
                    spacing: 6

                    model: params
                    
                    delegate: Component {
                        Loader {
                            id: param
                            source : model.object.paramType + ".qml"
                            width: parent.width
                            x: 15 // here is the distance to the left of the listview

                        }
                    }
                    ButtleScrollBar{
                        flickable: tuttleParam
                        vertical: true
                        hideScrollBarsWhenStopped: false

                    }
                    interactive: true
                }
            }

            //placed here to avoid a bug of display with the listView (should be displayed after the listview)
            Rectangle{
                id: tuttleParamTitle
                width: paramEditor.width
                height: 40
                color: paramEditor.background

                Text {
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.left: parent.left
                    anchors.leftMargin: 10
                    color: textColor
                    //font.underline: true
                    font.pointSize: 12
                    text: "Parameters"
                }

                gradient: Gradient {
                    GradientStop { position: 0.0; color: paramEditor.gradian2 }
                    GradientStop { position: 0.05; color: paramEditor.gradian1 }
                    GradientStop { position: 0.50; color: paramEditor.gradian1 }
                    GradientStop { position: 1; color: paramEditor.gradian2 }
                }
            }
        }

        /*BUTTLE PARAMS*/
        Rectangle{
            //Splitter.minimumHeight: buttleParamTitle.height
            id: buttleParams
            height: 190
            width: paramEditor.width
            color: paramEditor.background
            anchors.bottom: parent.bottom

            Rectangle{
                id: buttleParamTitle
                width: parent.width
                height: 40
                color: paramEditor.background

                Text {
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.left: parent.left
                    anchors.leftMargin: 10
                    color: textColor
                    //font.underline: true
                    font.pointSize: 12
                    text: "Node properties"
                }

                gradient: Gradient {
                    GradientStop { position: 0.0; color: paramEditor.gradian2 }
                    GradientStop { position: 0.05; color: paramEditor.gradian1 }
                    GradientStop { position: 0.50; color: paramEditor.gradian1 }
                    GradientStop { position: 1; color: paramEditor.gradian2 }
                }
            }

            Loader {
                sourceComponent: currentParamNode ? nodeParamComponent : undefined
                //anchors.fill: parent
                anchors.top: buttleParamTitle.bottom
                anchors.topMargin: 10
                Component {
                    id: nodeParamComponent
                    Column {
                        spacing: 5

                        /*Name of the node (Buttle data)*/
                        Item {
                            id: nodeNameUserItem
                            implicitWidth: 300
                            implicitHeight: 30
                            anchors.left: parent.left
                            anchors.leftMargin: 10

                            Row {
                                id: nodeNameUserContainer
                                spacing: 10

                                /* Title */
                                Text {
                                    id: nodeNameUserText
                                    width: 80
                                    anchors.top: parent.top
                                    anchors.verticalCenter: parent.verticalCenter
                                    color: textColor
                                    text: "Name : "
                                }

                                /* Input field limited to 50 characters */
                                Rectangle {
                                    height: 20
                                    implicitWidth: 200
                                    color: paramEditor.backgroundInput
                                    border.width: 1
                                    border.color: paramEditor.borderInput
                                    radius: 3
                                    TextInput {
                                        id: nodeNameUserInput
                                        text: currentParamNode.nameUser
                                        anchors.left: parent.left
                                        anchors.verticalCenter: parent.verticalCenter
                                        anchors.leftMargin: 5
                                        maximumLength: 100
                                        selectByMouse : true
                                        color: activeFocus ? activeFocusOn : activeFocusOff

                                        onAccepted: {
                                            currentParamNode.nameUser = nodeNameUserInput.text
                                            _buttleData.graphWrapper.updateConnectionsCoord()
                                        }
                                        onActiveFocusChanged: {
                                            currentParamNode.nameUser = nodeNameUserInput.text
                                            _buttleData.graphWrapper.updateConnectionsCoord()
                                        }

                                        KeyNavigation.backtab: nodeColorRGBInput
                                        KeyNavigation.tab: nodeCoordXInput


                                    }
                                }
                            }
                        }
                    
                        /* Type of the node (Buttle data) */
                        Item {
                            id: nodeTypeItem
                            implicitWidth: 300
                            implicitHeight: 30
                            anchors.left: parent.left
                            anchors.leftMargin: 10

                            Row {
                                id: nodeTypeContainer
                                spacing: 10

                                /* Title */
                                Text {
                                    id: nodeTypeText
                                    width: 80
                                    text: "Type : "
                                    color: textColor
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
                                        text: currentParamNode.nodeType
                                        anchors.left: parent.left
                                        anchors.leftMargin: 5
                                        color: "grey"
                                    }
                                }
                            }
                        }

                        /* Coord of the node (Buttle data) */
                        Item {
                            id: nodecoordItem
                            implicitWidth: 300
                            implicitHeight: 30
                            anchors.left: parent.left
                            anchors.leftMargin: 10

                            Row {
                                id: nodeCoordContainer
                                spacing: 10

                                /* Title */
                                Text {
                                    id: nodeCoordText
                                    width: 80
                                    text: "Coord : "
                                    color: textColor
                                    anchors.top: parent.top
                                    anchors.verticalCenter: parent.verticalCenter
                                }

                                /* Input label : "x : " */
                                Rectangle {
                                    height: 20
                                    implicitWidth: 15
                                    color: "transparent"
                                    Text{
                                        id: nodeCoordXLabel
                                        text: "x :"
                                        anchors.left: parent.left
                                        anchors.leftMargin: 5
                                        color: textColor
                                    }
                                }
                                /* Input field limited : x */
                                Rectangle {
                                    height: 20
                                    implicitWidth: 35
                                    color: paramEditor.backgroundInput
                                    border.width: 1
                                    border.color: paramEditor.borderInput
                                    radius: 3
                                    TextInput {
                                        id: nodeCoordXInput
                                        text: currentParamNode.coord.x
                                        anchors.left: parent.left
                                        anchors.leftMargin: 5
                                        color: activeFocus ? activeFocusOn : activeFocusOff
                                        selectByMouse : true

                                        onAccepted: {
                                            currentParamNode.coord.x = nodeCoordXInput.text
                                            _buttleData.graphWrapper.updateConnectionsCoord()
                                        }
                                        onActiveFocusChanged: {
                                            currentParamNode.coord.x = nodeCoordXInput.text
                                            _buttleData.graphWrapper.updateConnectionsCoord()
                                        }

                                        KeyNavigation.backtab: nodeNameUserInput
                                        KeyNavigation.tab: nodeCoordYInput

                                    }
                                }

                                /* Input label : "y : " */
                                Rectangle {
                                    height: 20
                                    implicitWidth: 15
                                    color: "transparent"
                                    Text{
                                        id: nodeCoordYLabel
                                        text: "y :"
                                        anchors.left: parent.left
                                        anchors.leftMargin: 5
                                        color: textColor
                                    }
                                }
                                /* Input field limited : y */
                                Rectangle {
                                    height: 20
                                    implicitWidth: 35
                                    color: paramEditor.backgroundInput
                                    border.width: 1
                                    border.color: paramEditor.borderInput
                                    radius: 3
                                    TextInput {
                                        id: nodeCoordYInput
                                        text: currentParamNode.coord.y
                                        anchors.left: parent.left
                                        anchors.leftMargin: 5
                                        color: activeFocus ? activeFocusOn : activeFocusOff
                                        selectByMouse : true

                                        onAccepted: {
                                            currentParamNode.coord.y = nodeCoordYInput.text
                                            _buttleData.graphWrapper.updateConnectionsCoord()
                                        }
                                        onActiveFocusChanged: {
                                            currentParamNode.coord.y = nodeCoordYInput.text
                                            _buttleData.graphWrapper.updateConnectionsCoord()
                                        }

                                        KeyNavigation.backtab: nodeCoordXInput
                                        KeyNavigation.tab: nodeColorRGBInput
                                    }
                                }
                            }
                        }

                        /* Color of the node (Buttle data) */
                        Item {
                            id: nodecolorItem
                            implicitWidth: 300
                            implicitHeight: 30
                            anchors.left: parent.left
                            anchors.leftMargin: 10

                            Row {
                                id: nodeColorContainer
                                spacing: 10

                                /* Title */
                                Text {
                                    id: nodeColorText
                                    width: 80
                                    text: "Color (Hex) : "
                                    color: textColor
                                    anchors.top: parent.top
                                    anchors.verticalCenter: parent.verticalCenter
                                }

                                /* Input field limited : rgb */
                                Rectangle {
                                    height: 20
                                    implicitWidth: 80
                                    color: paramEditor.backgroundInput
                                    border.width: 1
                                    border.color: paramEditor.borderInput
                                    radius: 3
                                    TextInput {
                                        id: nodeColorRGBInput
                                        text: currentParamNode.color
                                        anchors.left: parent.left
                                        anchors.verticalCenter: parent.verticalCenter
                                        anchors.leftMargin: 5
                                        maximumLength: 50
                                        selectByMouse : true
                                        color: activeFocus ? activeFocusOn : activeFocusOff

                                        onAccepted: currentParamNode.color = nodeColorRGBInput.text
                                        onActiveFocusChanged: currentParamNode.color = nodeColorRGBInput.text

                                        KeyNavigation.backtab: nodeCoordYInput
                                        KeyNavigation.tab: nodeNameUserInput
                                    }//textinput
                                }//rectangle of nodeColorContainer
                            }//row nodeColorContainer
                        }//item nodeColorItem
                    }//column
                }//component
            }//loader
        }//rectangle of buttleParam
    }//splitterColumn
}

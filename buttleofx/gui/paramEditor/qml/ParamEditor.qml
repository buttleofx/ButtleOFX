import QtQuick 2.0
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0

//parent of the ParamEditor is the Row of the ButtleAp
Item {
    id: paramEditor

    property variant params 
    property variant currentParamNode

    property color background: "#141414"
    property color backgroundInput: "#343434"
    property color gradian1: "#010101"
    property color gradian2: "#141414"
    property color borderInput: "#444"

    property color textColor : "white"
    property color activeFocusOn : "white"
    property color activeFocusOff : "grey"

    implicitWidth: 300
    implicitHeight: 500

    SplitView {
        width: parent.width
        height: parent.height
        //handleWidth: 3
        orientation: Qt.Vertical

        /*TUTTLE PARAMS*/
        Rectangle {
            Layout.minimumHeight: tuttleParamTitle.height

            id: tuttleParams
            height: 500
            width: parent.width
            color: paramEditor.background           

            /* Params depend on the node type (Tuttle data)*/
            Item {
                id: tuttleParamContent
                height: parent.height - tuttleParamTitle.height
                width: parent.width
                y: tuttleParamTitle.height

                property string lastGroupParam : "No Group."

                ScrollView {
                    anchors.fill: parent
                    anchors.topMargin: 5
                    anchors.bottomMargin: 5
                    height: 110
                    width: 110
                    //frame: false
                    // frameWidth: 0
                    ListView {
                        id: tuttleParam
                        height: count ? contentHeight : 0
                        y: parent.y + 10
                        spacing: 6

                        interactive: false

                        model: params
                        
                        delegate: Component {
                            Loader {
                                id: param
                                source : model.object.paramType + ".qml"
                                width: parent.width
                                x: 15 // here is the distance to the left of the listview
                            }
                        }
                    }//Listview
                }//scrollArea
            }//rectangle param

            //placed here to avoid a bug of display with the listView (should be displayed after the listview)
            Rectangle{
                id: tuttleParamTitle
                width: paramEditor.width
                height: 40
                color: paramEditor.background
                gradient: Gradient {
                    GradientStop { position: 0.0; color: gradian2 }
                    GradientStop { position: 0.85; color: gradian2 }
                    GradientStop { position: 0.86; color: gradian1 }
                    GradientStop { position: 1; color: gradian2 }
                } 

                Text {
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.left: parent.left
                    anchors.leftMargin: 10
                    color: textColor
                    font.pointSize: 11
                    text: "Parameters"
                }
            }
        }

        /*BUTTLE PARAMS*/
        Rectangle{
            Layout.minimumHeight: buttleParamTitle.height
            id: buttleParams
            anchors.bottom: parent.bottom
            height: 190
            width: paramEditor.width
            color: paramEditor.background

            Rectangle{
                id: buttleParamTitle
                width: parent.width
                height: 40
                color: paramEditor.background
                gradient: Gradient {
                    GradientStop { position: 0.0; color: gradian2 }
                    GradientStop { position: 0.85; color: gradian2 }
                    GradientStop { position: 0.86; color: gradian1 }
                    GradientStop { position: 1; color: gradian2 }
                } 

                Text {
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.left: parent.left
                    anchors.leftMargin: 10
                    color: textColor
                    font.pointSize: 11
                    text: "Node properties"
                }
            }

            Loader {
                sourceComponent: currentParamNode ? nodeParamComponent : undefined
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
                                spacing: 5

                                /* Title */
                                Text {
                                    id: nodeNameUserText
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
                                        text: currentParamNode ? currentParamNode.nameUser : ""
                                        anchors.left: parent.left
                                        width: parent.width - 10
                                        height: parent.height
                                        anchors.leftMargin: 5
                                        maximumLength: 100
                                        selectByMouse : true
                                        color: activeFocus ? activeFocusOn : activeFocusOff

                                        onAccepted: {
                                            currentParamNode.nameUser = nodeNameUserInput.text
                                        }
                                        onActiveFocusChanged: {
                                            currentParamNode.nameUser = nodeNameUserInput.text
                                        }

                                        KeyNavigation.backtab: nodeCoordYInput
                                        KeyNavigation.tab: nodeColorRGBInput
                                    }
                                    MouseArea {
                                        anchors.fill: parent
                                        acceptedButtons: Qt.RightButton
                                        onClicked: currentParamNode.nameUser = currentParamNode.getDefaultNameUser()
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
                                        text: currentParamNode ? currentParamNode.nodeType : ""
                                        anchors.left: parent.left
                                        anchors.leftMargin: 5
                                        color: "grey"
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
                                    text: "Color : "
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
                                        //text: currentParamNode ? currentParamNode.color : ""
                                        anchors.left: parent.left
                                        anchors.verticalCenter: parent.verticalCenter
                                        anchors.leftMargin: 5
                                        width: parent.width - 10
                                        height: parent.height
                                        maximumLength: 50
                                        selectByMouse : true
                                        color: activeFocus ? activeFocusOn : activeFocusOff

                                        onAccepted: currentParamNode.color = nodeColorRGBInput.text
                                        onActiveFocusChanged: currentParamNode.color = nodeColorRGBInput.text

                                        KeyNavigation.backtab: nodeNameUserInput
                                        KeyNavigation.tab: nodeCoordXInput
                                    }//textinput
                                    MouseArea {
                                        anchors.fill: parent
                                        acceptedButtons: Qt.RightButton
                                        onClicked: {
                                            currentParamNode.color = currentParamNode.getDefaultColor();
                                            console.log("Clicked");
                                        }
                                    }
                                }//rectangle of nodeColorContainer
                            }//row nodeColorContainer
                        }//item nodeColorItem

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
                                        text: currentParamNode ? currentParamNode.coord.x : ""
                                        anchors.left: parent.left
                                        anchors.leftMargin: 5
                                        width: parent.width - 10
                                        height: parent.height
                                        color: activeFocus ? activeFocusOn : activeFocusOff
                                        selectByMouse : true

                                        onAccepted: {
                                            currentParamNode.xCoord = nodeCoordXInput.text
                                        }
                                        onActiveFocusChanged: {
                                            currentParamNode.xCoord = nodeCoordXInput.text
                                        }

                                        KeyNavigation.backtab: nodeColorRGBInput
                                        KeyNavigation.tab: nodeCoordYInput

                                    }
                                }

                                /* Input label : "y : " */
                                Rectangle {
                                    height: 20
                                    implicitWidth: 15
                                    color: "transparent"
                                    Text {
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
                                        text: currentParamNode ? currentParamNode.coord.y : ""
                                        anchors.left: parent.left
                                        anchors.leftMargin: 5
                                        width: parent.width - 10
                                        height: parent.height
                                        color: activeFocus ? activeFocusOn : activeFocusOff
                                        selectByMouse : true

                                        onAccepted: {
                                            currentParamNode.yCoord = nodeCoordYInput.text
                                        }
                                        onActiveFocusChanged: {
                                            currentParamNode.yCoord = nodeCoordYInput.text
                                        }

                                        KeyNavigation.backtab: nodeCoordXInput
                                        KeyNavigation.tab: nodeNameUserInput
                                    }
                                }
                            }
                        }
                    }//column
                }//component
            }//loader
        }//rectangle of buttleParam
    }//splitterColumn
}

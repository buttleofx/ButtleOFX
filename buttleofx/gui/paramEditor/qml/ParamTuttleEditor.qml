import QtQuick 2.0
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0
import QtQuick.Controls.Styles 1.0
import "qmlComponents"

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
                y: tuttleParamTitle.height + 5

                property string lastGroupParam : "No Group."

                ScrollView {
                    anchors.fill: parent
                    anchors.topMargin: 5
                    anchors.bottomMargin: 5
                    height: 110
                    width: 110

                    style: ScrollViewStyle {
                        scrollBarBackground: Rectangle {
                            id: scrollBar
                            width:15
                            color: "#212121"
                            border.width: 1
                            border.color: "#333"
                        }
                        decrementControl : Rectangle {
                            id: scrollLower
                            width:15
                            height:15
                            color: styleData.pressed? "#212121" : "#343434"
                            border.width: 1
                            border.color: "#333"
                            radius: 3
                            Image{
                                id: arrow
                                source: "file:///" + _buttleData.buttlePath + "/gui/img/buttons/params/arrow2.png"
                                x:4
                                y:4
                            }
                        }
                        incrementControl : Rectangle {
                            id: scrollHigher
                            width:15
                            height:15
                            color: styleData.pressed? "#212121" : "#343434"
                            border.width: 1
                            border.color: "#333"
                            radius: 3
                            Image{
                                id: arrow
                                source: "file:///" + _buttleData.buttlePath + "/gui/img/buttons/params/arrow.png"
                                x:4
                                y:4
                            }
                        }
                    }


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
                                z:0

                                ToolTip{
                                    id:tooltip
                                    visible: false
                                    paramHelp: model.object.doc
                                    z:param.z+1
                                }
                                MouseArea {
                                    anchors.fill: parent
                                    acceptedButtons: Qt.RightButton               
                                    hoverEnabled:true
                                    onClicked: {
                                        model.object.hasChanged = false
                                        model.object.value = model.object.getDefaultValue()
                                        model.object.pushValue(model.object.value)
                                    }
                                    onEntered: {
                                        tooltip.visible=true
                                    }
                                    onExited: {
                                        tooltip.visible=false
                                    }
                                }
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
    }//splitterColumn
}

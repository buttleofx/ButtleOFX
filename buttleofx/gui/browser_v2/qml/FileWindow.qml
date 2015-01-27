import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Dialogs 1.0
import QtQuick.Layouts 1.0
import QtQuick.Controls.Styles 1.0

Rectangle {
    id: root

    color: "transparent"

    property var model
    property var visitedFolderList
    property int visitedFolderListIndex

    ScrollView {
        anchors.fill: parent

        style: ScrollViewStyle {
            scrollBarBackground: Rectangle {
                id: scrollBar
                width: styleData.hovered ? 8 : 4
                color: "transparent"

                Behavior on width { PropertyAnimation { easing.type: Easing.InOutQuad ; duration: 200 } }
            }

            handle: Item {
                implicitWidth: 15
                Rectangle {
                    color: "#00b2a1"
                    anchors.fill: parent
                }
            }

            decrementControl : Rectangle {
                visible: false
            }

            incrementControl : Rectangle {
                visible: false
            }
        }


        GridView {
            id: grid

            anchors.fill: parent

            cellWidth: 120
            cellHeight: 100

            // displayMarginBeginning: 20 // Available in QtQuick 2.3
            // displayMarginEnd: 20 // Available in QtQuick 2.3

            clip: true
            model: root.model.fileItems

            delegate: component
        }
    }

    Component {
        id: component

        Column {
            width: grid.cellWidth - 10
            height: grid.cellHeight - 10

            Image {
                id: icon

                anchors.horizontalCenter: parent.horizontalCenter

                source: model.object.pathImg
                sourceSize.width: 50
                sourceSize.height: 50
                fillMode: Image.PreserveAspectFit
            }

            Text {
                id: fileName

                width: parent.width

                anchors.horizontalCenter: parent.horizontalCenter
                horizontalAlignment: Text.AlignHCenter

                text: model.object.name
                color: (model.object.isSelected) ? "black" : "white"

                font.bold: model.object.isSelected

                wrapMode: Text.WrapAnywhere
                maximumLineCount: (model.object.isSelected) ? contentHeight : 2
            }

        }
    }

//    ScrollView {
//        Layout.fillHeight: true
//        Layout.fillWidth: true

//        style: ScrollViewStyle {
//            scrollBarBackground: Rectangle {
//                id: scrollBar
//                width: 15
//                height: parent.height
//                anchors.right: parent.right
//                color: "transparent"
//            }

//            decrementControl : Rectangle {
//                id: scrollLower
//                width: 15
//                height: 15
//                color: "#343434"

//                Image {
//                    id: arrowDown
//                    source: styleData.pressed ? "img/arrow_up_hover.png" : "img/arrow_up.png"
//                    anchors.horizontalCenter: parent.horizontalCenter
//                    anchors.verticalCenter: parent.verticalCenter
//                }
//            }

//            incrementControl : Rectangle {
//                id: scrollHigher
//                width: 15
//                height: 15
//                color: "#343434"

//                Image {
//                    id: arrowUp
//                    source: styleData.pressed ? "img/arrow_down_hover.png" : "img/arrow_down.png"
//                    anchors.horizontalCenter: parent.horizontalCenter
//                    anchors.verticalCenter: parent.verticalCenter
//                }
//            }
//        }

//        TableView {

//            id: listView
//            height: parent.height
//            width: parent.width

//            style: TableViewStyle {
//                scrollBarBackground: Rectangle {
//                    id: scrollBar
//                    width: 15
//                    height: parent.height
//                    anchors.right: parent.right
//                    color: "transparent"
//                }

//                decrementControl : Rectangle {
//                    id: scrollLower
//                    width: 15
//                    height: 15
//                    color: "#343434"

//                    Image {
//                        id: arrowDown
//                        source: styleData.pressed ? "img/arrow_up_hover.png" : "img/arrow_up.png"
//                        anchors.horizontalCenter: parent.horizontalCenter
//                        anchors.verticalCenter: parent.verticalCenter
//                    }
//                }

//                incrementControl : Rectangle {
//                    id: scrollHigher
//                    width: 15
//                    height: 15
//                    color: "#343434"

//                    Image {
//                        id: arrowUp
//                        source: styleData.pressed ? "img/arrow_down_hover.png" : "img/arrow_down.png"
//                        anchors.horizontalCenter: parent.horizontalCenter
//                        anchors.verticalCenter: parent.verticalCenter
//                    }
//                }
//            }

////            TableViewColumn {
////                title: "Owner"
////                role: name
////                visible: true
////            }

////            TableViewColumn {
////                title: "Name"

////            }

//            itemDelegate: Item {
//                Text {
//                    text: model.object.name
//                    color: styleData.textColor
//                }
//            }

//            onClicked: {
//                console.log(model.get(row).name)
//            }

//            model: root.model.fileItems
//        }
//    }
}


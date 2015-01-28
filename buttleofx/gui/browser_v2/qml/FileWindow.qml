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

            cellWidth: 150
            cellHeight: 100

            // displayMarginBeginning: 20 // Available in QtQuick 2.3
            // displayMarginEnd: 20 // Available in QtQuick 2.3

            clip: true
            model: root.model.fileItems

            delegate: component

            boundsBehavior: Flickable.StopAtBounds
            focus: true
        }

    }

    Component {
        id: component

        Rectangle {
            width: grid.cellWidth - 10
            height: grid.cellHeight - 30

            color: (model.object.isSelected) ? "#22FFFFFF" : "transparent"
            radius: 2

            Column {
                anchors.fill: parent

                Image {
                    id: icon

                    anchors.horizontalCenter: parent.horizontalCenter

                    source: model.object.pathImg
                    sourceSize.width: 50
                    sourceSize.height: 50
                    fillMode: Image.PreserveAspectFit

                    opacity: ((icon_mouseArea.containsMouse || text_mouseArea.containsMouse) ^ model.object.isSelected) ? 1 : 0.7

                    MouseArea {
                        id: icon_mouseArea
                        anchors.fill: parent

                        hoverEnabled: true

                        onClicked: {
                            if (!model.object.isSelected)
                                model.object.isSelected = true
                        }

                        onDoubleClicked: {
                            if (model.object.type === 1) { // Folder

                                if (visitedFolderList.count === 0){
                                    // Save path of the current folder
                                    visitedFolderList.append({"url": root.model.currentPath})
                                }

                                // Save path of the incoming folder
                                visitedFolderList.append({"url": model.object.path})
                                ++ visitedFolderListIndex

                                // Set the new path

                                root.model.currentPath = model.object.path
                            }
                        }
                    }
                }

                Text {
                    id: fileName

                    width: parent.width

                    elide: Text.ElideLeft
                    anchors.horizontalCenter: parent.horizontalCenter
                    horizontalAlignment: Text.AlignHCenter

                    text: model.object.name
                    color: ((icon_mouseArea.containsMouse || text_mouseArea.containsMouse) ^ model.object.isSelected) ? "white" : "#BBBBBB"

                    wrapMode: Text.WrapAnywhere
                    maximumLineCount: (model.object.isSelected) ? contentHeight : 2

                    MouseArea {
                        id: text_mouseArea
                        anchors.fill: parent

                        hoverEnabled: true

                        onClicked: {
                            if (!model.object.isSelected)
                                model.object.isSelected = true
                        }

                        onDoubleClicked: {
                            if (model.object.type === 1) { // Folder

                                if (visitedFolderList.count === 0){
                                    // Save path of the current folder
                                    visitedFolderList.append({"url": root.model.currentPath})
                                }

                                // Save path of the incoming folder
                                visitedFolderList.append({"url": model.object.path})
                                ++ visitedFolderListIndex

                                // Set the new path
                                root.model.currentPath = model.object.path
                            }
                        }
                    }
                }

                Component.onCompleted: {
                    fileName.width = fileName.paintedWidth
                }
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


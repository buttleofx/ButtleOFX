import QtQuick 2.0
import QtQuick.Layouts 1.0
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0

Rectangle {
    id: root

    width: 800
    height: 600

    color: "transparent"

    // Absolute path model
    // property alias model:

    Component {
        id: component

        RowLayout {
            width: folder.width + arrow.width
            height: parent.height

            Text {
                id: folder

                width: 100
                text: "display" // folder name

                anchors.verticalCenterOffset: parent.verticalCenter

                color: "red"

                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                }
            }

            Item {
                id: arrow

                width: 15
                height: parent.height

                Text {
                    text: ">"
                }
            }
            // TO DO add mouse area on the arrow to browse folders
        }
    }

    RowLayout {
        spacing: 6
        anchors.fill: parent
        anchors.leftMargin: spacing
        anchors.rightMargin: spacing

        Button {
            id: previous
            width: 15
            height: 15

            tooltip: "Previous"

            iconSource:
            if (hovered)
                "img/previous_hover.png"
            else
                "img/previous.png"

            style:
            ButtonStyle {
                background: Rectangle {
                    anchors.fill: parent
                    color: "transparent"
                }
            }

//            onClicked: {
//                if (listPrevious.count > 0) {
//                    nextList.append({"url": headerBar.folder})
//                    changeFolder(listPrevious.get(listPrevious.count - 1).url)
//                    listPrevious.remove(listPrevious.count - 1)
//                }
//            }
        }

        Button {
            id: next
            width: 15
            height: 15

            tooltip: "Next"

            iconSource:
            if (hovered)
                "img/next_hover.png"
            else
                "img/next.png"

            style:
            ButtonStyle {
                background: Rectangle {
                    anchors.fill: parent
                    color: "transparent"
                }
            }

//            onClicked: {
//                if (nextList.count > 0) {
//                    listPrevious.append({"url": headerBar.folder})
//                    changeFolder(nextList.get(nextList.count - 1).url)
//                    nextList.remove(nextList.count - 1)
//                }
//            }
        }

        Button {
            id: parent_folder
            width: 15
            height: 15

            tooltip: "Parent folder"

            iconSource:
            if (hovered)
                "img/parent_hover.png"
            else
                "img/parent.png"

            style:
            ButtonStyle {
                background: Rectangle {
                    anchors.fill: parent
                    color: "transparent"
                }
            }

//            onClicked: changeFolder(parentFolder)
        }

        Rectangle {
            id: textEditContainer
            height: 28
            Layout.fillWidth: true
            visible: false

            color: "#DDDDDD"
            border.color: "#00B2A1"
            border.width: 2
            radius: 3

            TextInput {
                id: texteditPath
                y: 5
                x: 5
                height: parent.height
                width: parent.width - 10
                clip: true

                text: "Lorem ipsum/Lorem"

                //color: suggestion.exists ? "white" : "red"
                selectByMouse: true
                selectionColor: "#00b2a1"

//                onAccepted: {
//                    if (acceptableInput) {
//                        listPrevious.append({"url": headerBar.folder})
//                        changeFolder(text)
//                        textEditContainer.forceActiveFocus()
//                    }
//                }

//                onFocusChanged: {
//                    if (texteditPath.focus) {
//                        if (!withTab) {
//                            selectAll()
//                        }
//                    } else {
//                        if (acceptableInput) {
//                            listPrevious.append({"url": headerBar.folder})
//                            changeFolder(text)
//                        }
//                    }
//                }
//                onTextChanged: {
//                    suggestion.folder = texteditPath.getText(0, texteditPath.cursorPosition + 1)
//                }
//                onCursorPositionChanged: {
//                    suggestion.folder = texteditPath.getText(0, texteditPath.cursorPosition + 1)
//                }

//                validator: RegExpValidator {
//                    regExp:
//                    if (!suggestion.isEmpty()) {
//                            /suggestion.getFilteredFileItems(suggestion.folder).get(0).filepath/
//                    } else {
//                            /.*/
//                    }
//                }

//                Keys.onTabPressed: {
//                    suggestionsMenu.show()
//                    texteditPath.forceActiveFocus()
//                }
            }
        }

        ListView {
           id: breadCrum

           Layout.fillWidth: true
           height: parent.height
           orientation: Qt.Horizontal

           visible: true

           delegate: component

           MouseArea {
               anchors.fill: parent

               onClicked: {
                   if (breadCrum.visible)
                       breadCrum.visible = false

                   if (!textEditContainer.visible)
                       textEditContainer.visible = true
               }
           }
       }

        Button {
            id: refresh
            width: 15
            height: 15

            tooltip: "Refresh"

            iconSource:
            if (hovered)
                "img/refresh_hover.png"
            else
                "img/refresh.png"

            style:
            ButtonStyle {
                background: Rectangle {
                    anchors.fill: parent
                    color: "transparent"
                }
            }

            // onClicked: refreshFolder()
        }

        Button {
            id: view
            width: 15
            height: 15

            tooltip: "List view"

            iconSource:
            if (hovered)
                "img/listview_hover.png"
            else
                "img/listview.png"

            states: [
                State {
                    name: "gridview"
//                    when: headerBar.isInListView == true
                    PropertyChanges {
                        target: view
                        tooltip: "List view"
                        iconSource:
                        if (hovered)
                            "img/gridview_hover.png"
                        else
                            "img/gridview.png"
                    }
                },
                State {
                    name: "listview"
//                    when: headerBar.isInListView == false
                    PropertyChanges {
                        target: view
                        tooltip: "Grid view"
                        iconSource:
                        if (hovered)
                            "img/listview_hover.png"
                        else
                            "img/listview.png"
                    }
                }
            ]

            style:
            ButtonStyle {
                background: Rectangle {
                    anchors.fill: parent
                    color: "transparent"
                }
            }

//            onClicked:
//            if (isInListView) {
//                isInListView = false
//            } else {
//                isInListView = true
//            }
        }
    }
}


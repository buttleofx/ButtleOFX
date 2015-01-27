import QtQuick 2.2
import QtQuick.Layouts 1.0
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0

// Navbar glogal struct
Rectangle {
    id: root

    color: "#2E2E2E"

    property var model
    property var visitedFolderList
    property int visitedFolderListIndex: 0

    RowLayout {
        anchors.fill: parent
        anchors.margins: 5
        spacing: 10

        Button {
            id: previous

            Layout.preferredWidth: 20
            Layout.preferredHeight: 20
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

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

            onClicked: {
                if (visitedFolderList.count > 1 && visitedFolderListIndex !== 0) {
                    -- visitedFolderListIndex
                    model.currentPath = visitedFolderList.get(visitedFolderListIndex).url
                }
            }
        }

        Button {
            id: next

            Layout.preferredWidth: 20
            Layout.preferredHeight: 20
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

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

            onClicked: {
                if (visitedFolderList.count > 1 && visitedFolderListIndex !== (visitedFolderList.count - 1)){
                    ++ visitedFolderListIndex
                    model.currentPath = visitedFolderList.get(visitedFolderListIndex).url
                }
            }
        }

        Button {
            id: parent_folder

            Layout.preferredWidth: 20
            Layout.preferredHeight: 20
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

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

            onClicked: {
                if (visitedFolderList.count === 0){
                    // Save path of the current folder
                    visitedFolderList.append({"url": model.currentPath})
                }

                // Test if the current path is not root
                if(visitedFolderList.get(visitedFolderListIndex).url !== "/") {

                    // Save path of the incoming folder
                    visitedFolderList.append({"url": model.parentFolder})
                    ++ visitedFolderListIndex

                    // Set the new path
                    model.currentPath = model.parentFolder
                }
            }
        }

        Button {
            id: refresh

            Layout.preferredWidth: 20
            Layout.preferredHeight: 20
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

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


        Rectangle {
            id: textEditContainer

            Layout.preferredHeight: parent.height
            Layout.fillWidth: true

            visible: false

            color: "#DDDDDD"
            border.color: "#00B2A1"
            border.width: 2
            radius: 3

            TextInput {
                id: texteditPath
                y: 5
                x: 10
                height: parent.height
                width: parent.width - 10
                clip: true

                text: root.model.currentPath

                //color: suggestion.exists ? "white" : "red"
                selectByMouse: true
                selectionColor: "#00b2a1"

                onAccepted: {
                    if (acceptableInput) {
                        if (visitedFolderList.count === 0){
                            // Save path of the current folder
                            visitedFolderList.append({"url": model.currentPath})
                        }

                        // Test if the current path is not root
                        if(visitedFolderList.get(visitedFolderListIndex).url !== "/") {

                            // Save path of the incoming folder
                            visitedFolderList.append({"url": text})
                            ++ visitedFolderListIndex

                            // Set the new path
                            model.currentPath = text
                        }
                    }
                }

//                onFocusChanged: {
//                    if (texteditPath.focus) {
//                        if (!withTab) {
//                            selectAll()
//                        }
//                    } else {
//                        if (acceptableInput) {
//                            visitedFolderList.append({"url": headerBar.folder})
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
           Layout.preferredHeight: parent.height

           orientation: Qt.Horizontal

           model: root.model.splitedCurrentPath

           visible: true
           clip: true

           MouseArea {
               anchors.fill: parent
               propagateComposedEvents: true
               onDoubleClicked: {
                   if (breadCrum.visible)
                       breadCrum.visible = false

                   if (!textEditContainer.visible)
                       textEditContainer.visible = true
               }
           }
           delegate: component
       }

        Button {
            id: view

            Layout.preferredWidth: 20
            Layout.preferredHeight: 20
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

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
    // One breadcrum component struct
    Component {
        id: component

        RowLayout {
            width: folder.width + arrow.width + 10
            height: parent.height

            Text {
                id: folder

                anchors.left: parent.left
                anchors.leftMargin: 5

                text: model.object[1]
                font.pointSize: 12
                color: (text_mouseArea.containsMouse) ? "white" : "#BBBBBB"

                MouseArea {
                    id: text_mouseArea
                    anchors.fill: parent
                    hoverEnabled: true
                    onClicked: {
                        if (visitedFolderList.count === 0){
                            // Save path of the current folder
                            visitedFolderList.append({"url": root.model.currentPath})
                        }

                        // Test if the clicked path is not the current
                        if(visitedFolderList.get(visitedFolderListIndex).url !== model.object[0]) {

                            // Save path of the incoming folder
                            visitedFolderList.append({"url": model.object[0]})
                            ++ visitedFolderListIndex

                            // Set the new path
                            root.model.currentPath = model.object[0]
                        }
                    }
                }
            }

            Item {
                id: arrow

                width: 20
                height: parent.height

                Text {
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.horizontalCenter: parent.horizontalCenter

                    text: ">"
                    font.pointSize: 16
                    font.bold: (arrow_mouseArea.containsMouse) ? true : false
                    color: "#00b2a1"

                    MouseArea {
                        id: arrow_mouseArea
                        anchors.fill: parent
                        hoverEnabled: true
                        onClicked: {
                            console.log("Arrow clicked")
                        }
                    }
                }
            }
        }
    }
}

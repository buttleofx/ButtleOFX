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
    signal autoCompleteMode(bool active)
    Layout.preferredHeight: searchLayoutRectangle.height+ navBarContainer.height

    function pushVisitedFolder(path){
        if (visitedFolderList.count === 0){
            // Save path of the current folder
            visitedFolderList.append({"url": root.model.currentPath})
        }

        visitedFolderList.append({"url": path})
        ++ visitedFolderListIndex
    }


    onAutoCompleteMode: {
        autoCompleteList.show()
    }

    ColumnLayout{
        anchors.fill: parent
        spacing: 0

        Rectangle{
            Layout.alignment: Qt.AlignTop
            id: navBarContainer
            Layout.fillWidth: true
            color: "transparent"
            Layout.preferredHeight: 50

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
                        if (visitedFolderList.count > 0 && visitedFolderListIndex > 0) {
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
                        if(visitedFolderList.get(visitedFolderListIndex).url !== "/") {
                            root.pushVisitedFolder(model.parentFolder)
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

                    onClicked: root.model.refresh()
                }


                Rectangle {
                    id: textEditContainer

                    Layout.preferredHeight: parent.height - 10
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

                        selectByMouse: true
                        selectionColor: "#00b2a1"

                        onTextChanged: {

                        }

                        onAccepted: {
                            root.model.currentPath = text
                            autoCompleteList.show()
                        }

                        Keys.onEscapePressed: {
                            if (!breadCrum.visible)
                                breadCrum.visible = true
                                breadCrum.forceActiveFocus()

                            if (textEditContainer.visible)
                                textEditContainer.visible = false

                        }

                        Keys.onDownPressed: {
                            autoCompleteList.show()
                        }

                        Keys.onTabPressed: {
                            root.model.currentPath = text
                            autoCompleteList.show()
                        }

                        Keys.onPressed: {
                            if ((event.key == Qt.Key_Space) && (event.modifiers & Qt.ControlModifier)){
                                autoCompleteList.show()
                                if(autoCompleteList.items.count > 0)
                                    autoCompleteList.items[0].trigger()
                            }
                            else{
                                model.currentPath = text
                            }
                        }

                        Menu {
                            id: autoCompleteList
                            Instantiator{
                                model:root.model.listFolderNavBar

                                MenuItem {

                                    id: textComponent
                                    text: model.object.name

                                    onTriggered: {
                                        root.pushVisitedFolder( model.object.path)
                                        root.model.currentPath = model.object.path
                                    }
                                }

                                onObjectAdded: autoCompleteList.insertItem(index, object)
                                onObjectRemoved: autoCompleteList.removeItem(object)
                            }

                            function show() {
                                // Retrieve position instead of cursorRectangle.x
                                root.model.currentPath = root.model.currentPath

                                if(!root.model.listFolderNavBar.count)
                                    return

                                var index = root.model.currentPath.length
                                var x = 0
                                var y = texteditPath.height

                                if (index != -1) {
                                    var rect = texteditPath.positionToRectangle(index)
                                    x = rect.x
                                }
                                this.__popup(x+textEditContainer.x+12, y)
                            }
                        }
                    }
                }

                ListView {
                   id: breadCrum

                   Layout.fillWidth: true
                   Layout.preferredHeight: parent.height

                   orientation: Qt.Horizontal

                   model: root.model.splittedCurrentPath

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
                                texteditPath.forceActiveFocus()
                       }
                   }
                   delegate: component
                }

                Button {
                    id: search

                    Layout.preferredWidth: 20
                    Layout.preferredHeight: 20
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

                    tooltip: "Search recursively"

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
                    onClicked: {
                        searchLayoutRectangle.visible = !searchLayoutRectangle.visible
                        searchEdit.forceActiveFocus()
                    }

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

                }
            }

        }

        Rectangle{
            id: searchLayoutRectangle
            Layout.fillWidth: true
            height: visible ? 35: 0
            color: "transparent"
            visible: false

            RowLayout{
                id: searchLayout
                anchors.fill: parent

                Rectangle {
                    id: searchContainer
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    visible: parent.visible
                    color: "#DDDDDD"
                    border.color: "#00B2A1"
                    border.width: 2
                    radius: 3

                    TextInput {
                        id: searchEdit
                        y: 5
                        x: 10
                        height: parent.height
                        width: parent.width - 10
                        clip: true
                        selectByMouse: true
                        selectionColor: "#00b2a1"

                        onAccepted: {
                            browser.doSearchRecursive(text)
                        }
                    }
                }
            }

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
                        root.pushVisitedFolder(model.object[0])
                        root.model.currentPath = model.object[0]

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
                    visible: !(index == (breadCrum.count - 1) && index != 0)

                    MouseArea {
                        id: arrow_mouseArea
                        anchors.fill: parent
                        hoverEnabled: true
                        onClicked: {
                            root.model.currentPath = model.object[0]
                        }
                    }
                }
            }
        }
    }
}

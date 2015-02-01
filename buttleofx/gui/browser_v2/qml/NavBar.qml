import QtQuick 2.2
import QtQuick.Layouts 1.0
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0

// Navbar glogal struct
Rectangle {
    id: root
    color: "#2E2E2E"
    clip: true
    Layout.preferredHeight: searchLayoutRectangle.height+ navBarContainer.height
    signal pushVisitedFolder(string path)

    ColumnLayout{
        anchors.fill: parent
        spacing: 0

        Rectangle{
            id: navBarContainer
            Layout.alignment: Qt.AlignTop
            Layout.fillWidth: true
            color: "transparent"
            Layout.preferredHeight: 40

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
                        if(model.currentPath !== "/" && model.currentPath.trim() !== ""){
                            pushVisitedFolder(model.parentFolder)
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

                    Layout.preferredHeight: parent.height - 2
                    Layout.fillWidth: true
                    visible: false

                    color: "#DDDDDD"
                    border.color: "#00B2A1"
                    border.width: 2
                    radius: 3

                    function hide(){
                        textEditContainer.visible = false
                        breadCrum.visible = true
                        breadCrum.forceActiveFocus()
                    }

                    TextInput {
                        id: texteditPath
                        height: parent.height
                        width: parent.width - 10
                        x: 10
                        y: 5

                        clip: true
                        text: root.model.currentPath

                        selectByMouse: true
                        selectionColor: "#00b2a1"

                        //address not empty at the beginning
                        validator: RegExpValidator{
                            regExp: /^[^\s]$/
                        }

                        Keys.onEscapePressed: {
                            textEditContainer.hide()
                        }

                        Keys.onTabPressed:{
                            if(autoCompleteList.items.length == 1)
                                autoCompleteList.items[0].trigger()
                            else
                                autoCompleteList.show()
                        }

                        Keys.onReleased: {
                            root.model.currentPath = texteditPath.text
                            if (((event.key == Qt.Key_Space) && (event.modifiers & Qt.ControlModifier))){
                                if(autoCompleteList.items.length == 1)
                                    autoCompleteList.items[0].trigger()
                            }
                            if(event.key == Qt.Key_Enter || event.key == Qt.Key_Return || event.key == Qt.Key_Down || (event.key == Qt.Key_Space))
                                autoCompleteList.show()
                        }

                        onFocusChanged: {
                            if(!focus)
                                textEditContainer.hide()
                        }

                        Menu {
                            id: autoCompleteList
                            __visualItem: textEditContainer //simulate container for popup

                            Instantiator{
                                model:root.model.listFolderNavBar

                                MenuItem {

                                    id: textComponent
                                    text: model.object.name

                                    onTriggered: {
                                        pushVisitedFolder( model.object.path)
                                        root.model.currentPath = model.object.path
                                    }
                                }

                                onObjectAdded: autoCompleteList.insertItem(index, object)
                                onObjectRemoved: autoCompleteList.removeItem(object)
                            }

                            function show() {
                                root.model.currentPath = texteditPath.text

                                if(!root.model.listFolderNavBar.count)
                                    return

                                var indexPosition = root.model.currentPath.length
                                var positionToShow = Qt.vector2d(0, texteditPath.height)
                                positionToShow.x = texteditPath.positionToRectangle(indexPosition).x
                                this.__popup(positionToShow.x+12, positionToShow.y)
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
                    iconSource: hovered ?"img/find_hover.png" : "img/find.png"
                    style:
                        ButtonStyle {
                            background: Rectangle {
                                anchors.fill: parent
                                color: "transparent"
                            }
                        }
                    onClicked: {
                        searchLayoutRectangle.enabled = !searchLayoutRectangle.enabled
                        searchEdit.forceActiveFocus()
                    }

                }

//                Button {
//                    id: view

//                    Layout.preferredWidth: 20
//                    Layout.preferredHeight: 20
//                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

//                    tooltip: "List view"

//                    iconSource:
//                    if (hovered)
//                        "img/listview_hover.png"
//                    else
//                        "img/listview.png"

//                    states: [
//                        State {
//                            name: "gridview"
//                            PropertyChanges {
//                                target: view
//                                tooltip: "List view"
//                                iconSource:
//                                if (hovered)
//                                    "img/gridview_hover.png"
//                                else
//                                    "img/gridview.png"
//                            }
//                        },
//                        State {
//                            name: "listview"
//                            PropertyChanges {
//                                target: view
//                                tooltip: "Grid view"
//                                iconSource:
//                                if (hovered)
//                                    "img/listview_hover.png"
//                                else
//                                    "img/listview.png"
//                            }
//                        }
//                    ]

//                    style:
//                    ButtonStyle {
//                        background: Rectangle {
//                            anchors.fill: parent
//                            color: "transparent"
//                        }
//                    }

//                }
            }

        }
        Rectangle{
            id: searchLayoutRectangle

            property bool enabled: true

            Layout.fillWidth: true
            height: enabled ? 30 : 0
            color: "transparent"

            Behavior on height { PropertyAnimation { easing.type: Easing.InOutQuad ; duration: 300 } }

            RowLayout{
                id: searchLayout
                anchors.fill: parent

                Rectangle {
                    id: searchContainer
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    color: "transparent"

                    TextField {
                        id: searchEdit

                        anchors.fill: parent
                        anchors.margins: 2
                        placeholderText: "Enter your search ..."

                        style: TextFieldStyle {
                                selectionColor: "#00b2a1"
                                textColor: "#2E2E2E"
                                background: Rectangle {
                                    color: "#DDDDDD"
                                    border.color: "#00b2a1"
                                    border.width: 1
                                }
                            }
                        onAccepted: {
                            if(text.trim())
                                _browser.doSearchRecursive(text.trim())
                        }

                        onFocusChanged: {
                            if(!focus)
                                searchLayoutRectangle.enabled = false
                        }
                    }
                }
            }
            Component.onCompleted: enabled = false
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
                        pushVisitedFolder(model.object[0])
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
                    font.bold: arrow_mouseArea.containsMouse
                    color: "#00b2a1"
                    visible: !(index == (breadCrum.count - 1) && index != 0)

                    MouseArea {
                        id: arrow_mouseArea
                        anchors.fill: parent
                        hoverEnabled: true
                        onClicked: {
                            pushVisitedFolder(model.object[0])
                            root.model.currentPath = model.object[0]
                        }
                    }
                }
            }
        }
    }
}

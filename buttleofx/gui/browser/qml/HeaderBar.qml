import QtQuick 2.1
import ButtleFileModel 1.0
import QtQuick.Layouts 1.0
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0


Rectangle {
    id: headerBar
    color: "#141414"

    property string folder
    signal changeFolder(string folder)
    signal refreshFolder()
    property string parentFolder
    property variant listPrevious
    property bool isInListView : false
    signal changeSeq(bool seq)
    property bool withTab: false

    function forceActiveFocusOnPath() {
        withTab = false
        texteditPath.forceActiveFocus()
    }

    function forceActiveFocusOnPathWithTab() {
        withTab = true
        texteditPath.forceActiveFocus()
    }

    FileModelBrowser {
        id: suggestion
        folder: headerBar.folder
    }

    ListModel {
        id: nextList
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

            iconSource:
            if (hovered) {
                "../../img/buttons/browser/previous_hover.png"
            } else {
                "../../img/buttons/browser/previous.png"
            }

            style:
            ButtonStyle {
                background: Rectangle {
                    anchors.fill: parent
                    color: "transparent"
                }
            }

            onClicked: {
                if (listPrevious.count > 0) {
                    nextList.append({"url": headerBar.folder})
                    changeFolder(listPrevious.get(listPrevious.count - 1).url)
                    listPrevious.remove(listPrevious.count - 1)
                }
            }
        }

        Button {
            id: next
            width: 15
            height: 15

            iconSource:
            if (hovered) {
                "../../img/buttons/browser/next_hover.png"
            } else {
                "../../img/buttons/browser/next.png"
            }

            style:
            ButtonStyle {
                background: Rectangle {
                    anchors.fill: parent
                    color: "transparent"
                }
            }

            onClicked: {
                if (nextList.count > 0) {
                    listPrevious.append({"url": headerBar.folder})
                    changeFolder(nextList.get(nextList.count - 1).url)
                    nextList.remove(nextList.count - 1)
                }
            }
        }

        Button {
            id: parent_folder
            width: 15
            height: 15

            iconSource:
            if (hovered) {
                "../../img/buttons/browser/parent_hover.png"
            } else {
                "../../img/buttons/browser/parent.png"
            }

            style:
            ButtonStyle {
                background: Rectangle {
                    anchors.fill: parent
                    color: "transparent"
                }
            }

            onClicked: changeFolder(parentFolder)
        }

        Rectangle {
            id: textEditContainer
            height: 24
            Layout.fillWidth: true

            color: "black"
            border.color: "grey"
            radius: 5

            TextInput {
                id: texteditPath
                y: 4
                x: 5
                height: parent.height
                width: parent.width - 10
                clip: true

                text: headerBar.folder

                color: suggestion.exists ? "white" : "red"
                selectByMouse: true
                selectionColor: "#00b2a1"

                onAccepted: {
                    if (acceptableInput) {
                        listPrevious.append({"url": headerBar.folder})
                        changeFolder(text)
                        textEditContainer.forceActiveFocus()
                    }
                }

                onFocusChanged: {
                    if (texteditPath.focus) {
                        if (!withTab) {
                            selectAll()
                        }
                    } else {
                        if (acceptableInput) {
                            listPrevious.append({"url": headerBar.folder})
                            changeFolder(text)
                        }
                    }
                }
                onTextChanged: {
                    suggestion.folder = texteditPath.getText(0, texteditPath.cursorPosition + 1)
                }
                onCursorPositionChanged: {
                    suggestion.folder = texteditPath.getText(0, texteditPath.cursorPosition + 1)
                }

                validator: RegExpValidator {
                    regExp:
                    if (!suggestion.isEmpty()) {
                            /suggestion.getFilteredFileItems(suggestion.folder).get(0).filepath/
                    } else {
                            /.*/
                    }
                }

                Keys.onTabPressed: {
                    suggestionsMenu.show()
                    texteditPath.forceActiveFocus()
                }
            }

            Menu {
                id: suggestionsMenu
                // __minimumWidth: textEditContainer.width
                // __xOffset: -13  // don't know how to remove icon space on menuItems
                // __yOffset: 0
                __visualItem: textEditContainer
                // style: __style.__popupStyle  //__style.__dropDownStyle

                // property ExclusiveGroup eg: ExclusiveGroup { id: eg }

                Instantiator {
                    model: suggestion.getFilteredFileItems(suggestion.folder)

                    MenuItem {
                        id: textComponent
                        text: model.object.fileName

                        onTriggered: {
                            changeFolder(model.object.filepath)
                        }
                        // checkable: true
                        // exclusiveGroup: eg
                    }

                    onObjectAdded: suggestionsMenu.insertItem(index, object)
                    onObjectRemoved: suggestionsMenu.removeItem(object)
                }

                function show() {
                    // Retrieve position of last "/" instead of cursorRectangle.x
                    var index = suggestion.folder.lastIndexOf("/")
                    var x = 0
                    if (index != -1) {
                        var rect = texteditPath.positionToRectangle(index)
                        x = rect.x
                    }

                    var y = texteditPath.height
                    suggestionsMenu.__popup(x, y)
                }
            }
        }

        Button {
            id: refresh
            width: 1
            height: 1

            iconSource:
            if (hovered) {
                "../../img/buttons/browser/refresh_hover.png"
            } else {
                "../../img/buttons/browser/refresh.png"
            }

            style:
            ButtonStyle {
                background: Rectangle {
                    anchors.fill: parent
                    color: "transparent"
                }
            }

            onClicked: refreshFolder()
        }

        Button {
            id: view
            width: 12
            height: 12

            iconSource:
            if (hovered) {
                "../../img/buttons/browser/listview_hover.png"
            } else {
                "../../img/buttons/browser/listview.png"
            }

            states: [
                State {
                    name: "gridview"
                    when: headerBar.isInListView == true
                    PropertyChanges {
                        target: view
                        iconSource:
                        if (hovered) {
                            "../../img/buttons/browser/gridview_hover.png"
                        } else {
                            "../../img/buttons/browser/gridview.png"
                        }
                    }
                },
                State {
                    name: "listview"
                    when: headerBar.isInListView == false
                    PropertyChanges {
                        target: view
                        iconSource:
                        if (hovered) {
                            "../../img/buttons/browser/listview_hover.png"
                        } else {
                            "../../img/buttons/browser/listview.png"
                        }
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

            onClicked:
            if (isInListView) {
                isInListView = false
            } else {
                isInListView = true
            }
        }

        CheckBox {
            id: check

            style: CheckBoxStyle {
                label: Text {
                    text: "Seq"
                    color: "white"
                }
            }

            onClicked: headerBar.changeSeq(check.checked)
        }
    }
}

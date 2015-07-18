import QtQuick 2.2
import QtQuick.Layouts 1.0
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0

// Navbar glogal struct
Rectangle {
    id: root
    color: "#2E2E2E"
    clip: true

    signal pushVisitedFolder(string path)
    property alias searchLayout: searchLayoutRectangle

    function toggleUrlEdit(visibility){
        visibility = visibility !== undefined ? visibility : breadCrum.visible
        breadCrum.visible = !visibility
        textEditContainer.visible = visibility

        if(visibility)
            texteditPath.forceActiveFocus()
    }

    Component.onCompleted: toggleUrlEdit(true)

    QtObject {
        id: m;
        property bool searchEnabled: false
    }

    Column{
        height: childrenRect.height

        Rectangle{
            id: navBarContainer

            width: root.width
            height: 40

            color: "transparent"


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
                    iconSource: hovered ? "img/previous_hover.png" : "img/previous.png"

                    style:
                        ButtonStyle {
                            background: Rectangle {
                                anchors.fill: parent
                                color: "transparent"
                            }
                        }

                    onClicked: popVisitedFolder()
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

                    iconSource: hovered ? "img/parent_hover.png" : "img/parent.png"

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

                Rectangle {
                    id: refresh

                    Layout.preferredWidth: 14
                    Layout.preferredHeight: 14
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    color: 'transparent'

                    MouseArea{
                        id: refreshMouse
                        anchors.fill: parent
                        hoverEnabled: true
                        onClicked: root.model.refresh()
                    }

                    Image {
                        id: modelLoading
                        anchors.fill: parent
                        source: refreshMouse.containsMouse || refreshRotation.running ? "img/refresh_hover.png" : 'img/refresh.png'
                        asynchronous: true

                        NumberAnimation on rotation {
                            id: refreshRotation
                            from: 0
                            to: 360
                            running: root.model.loading
                            loops: Animation.Infinite
                            duration: 1000
                            alwaysRunToEnd: true
                        }
                    }

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

                        //hack for position of graySuggestion: doesn't replace while typing
                        onCursorPositionChanged: {
                            graySuggestion.x = texteditPath.positionToRectangle(texteditPath.length).x
                        }

                        function handleFilter(){
                            var lastSlash = root.model.currentPath.lastIndexOf("/")
                            var indexOfWildcard = root.model.currentPath.indexOf("*")

                            if(indexOfWildcard && indexOfWildcard>lastSlash){
                                var filter=root.model.currentPath.substr(lastSlash+1)
                                root.model.currentPath = root.model.currentPath.substr(0,lastSlash)
                                root.model.filter =  filter
                            }
                            else
                                root.model.filter = "*"
                        }

                        Text{
                            id:graySuggestion
                            color:"gray"
                            property var listenerCurrentPath: root.model.currentPath
                            onListenerCurrentPathChanged: this.clear()

                            Behavior on x {
                                PropertyAnimation {
                                    easing.type: Easing.InOutQuad;
                                    duration: (graySuggestion.text.length)? 10:500
                                }
                            }

                            function setFormatted(name){
                                //more readable
                                var lastSlash = root.model.currentPath.lastIndexOf("/")
                                var lengthCurrentPath = root.model.currentPath.length

                                graySuggestion.text = name.substr((lengthCurrentPath -1 )- lastSlash)
                            }

                            function fill(){
                                this.clear()
                                if(root.model.listFolderNavBar.count === 1 && texteditPath.text.trim())
                                    this.setFormatted(root.model.listFolderNavBar.get(0)[0])

                            }

                            function clear(){
                                this.text = ""
                            }
                        }

                        //address not empty at the beginning
                        validator: RegExpValidator{
                            regExp: /^[^\s]{1,}/
                        }

                        Keys.onEscapePressed: {
                            textEditContainer.hide()
                        }

                        //need this event and not Keys.onPressed: have good behavior with tab key(which loose focus otherwise even if propagation stopped)
                        Keys.onTabPressed:{
                            autoCompleteList.handleInteraction()
                        }

                        Keys.onPressed: {
                            if((this.cursorPosition == this.text.length && event.key == Qt.Key_Right) ||
                               ((event.modifiers & Qt.ControlModifier)  && event.key == Qt.Key_Space))
                                autoCompleteList.handleInteraction()
                        }

                        Keys.onReleased: {
                            if(event.key === Qt.Key_Shift || event.key === Qt.Key_Alt || event.key === Qt.Key_Control
                               || (event.key === Qt.Key_Control && event.key === Qt.Key_L))
                                return
                            root.model.currentPath = texteditPath.text
                            graySuggestion.fill()

                            if(event.key === Qt.Key_Enter || event.key === Qt.Key_Return)
                                texteditPath.handleFilter()

                            if(event.key == Qt.Key_Down)
                                autoCompleteList.handleInteraction()
                        }

                        onFocusChanged: {
                            if(!focus){
                                graySuggestion.clear()
                                textEditContainer.hide()
                            }
                        }

                        Menu {
                            id: autoCompleteList
                            __visualItem: texteditPath
                            __xOffset: texteditPath.positionToRectangle(root.model.currentPath.length).x
                            __yOffset: texteditPath.height-8

                            Instantiator{
                                model:root.model.listFolderNavBar

                                MenuItem {
                                    id: textComponent
                                    text: model.object[0]
                                    property var path: model.object[1]

                                    onTriggered: {
                                        pushVisitedFolder(textComponent.path)
                                        graySuggestion.clear()
                                        root.model.currentPath = textComponent.path+"/"
                                    }
                                }
                                onObjectAdded: autoCompleteList.insertItem(index, object)
                                onObjectRemoved: autoCompleteList.removeItem(object)
                            }

                            function handleInteraction(){
                                if(autoCompleteList.items.length === 1)
                                      autoCompleteList.items[0].trigger()
                                else
                                    autoCompleteList.show()
                            }

                            function show() {
                                if(!root.model.listFolderNavBar.count)
                                    return
                                this.__popup(0, 0)
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
                            root.toggleUrlEdit()
                       }
                   }
                   delegate: component
                }

                Button {
                    id: show_seq

                    Layout.preferredWidth: 20
                    Layout.preferredHeight: 20
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    implicitHeight: 20
                    implicitWidth: 20

                    tooltip: "Toggle sequence mode"
                    iconSource: root.model.showSequence ? "img/gridview.png" : "img/gridview_hover.png"

                    style:
                    ButtonStyle {
                        background: Rectangle {
                            anchors.fill: parent
                            color: "transparent"
                        }
                    }

                    onClicked: {
                        root.model.setShowSequence(!root.model.showSequence)
                    }
                }


                Button {
                    id: action_button
                    property bool isOpen: false

                    Layout.preferredWidth: 20
                    Layout.preferredHeight: 20
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

                    tooltip: "Actions"

                    iconSource: hovered ? "img/listview_hover.png" : "img/listview.png"

                    style:
                    ButtonStyle {
                        background: Rectangle {
                            anchors.fill: parent
                            color: "transparent"
                        }
                    }

                    onClicked: {
                        if (!isOpen) {
                            var component = Qt.createComponent("ActionManager.qml")
                            var window    = component.createObject(root)
                            window.show()
                            isOpen = true
                        }
                    }
                }

                Button {
                    id: search
                    Layout.preferredWidth: 30
                    Layout.preferredHeight: 30

                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

                    tooltip: "Search recursively"
                    iconSource: hovered ?"img/find_hover.png" : "img/find.png"

                    style:
                        ButtonStyle {
                            background: Rectangle {
                                anchors.fill: parent
                                radius: 2
                                color: m.searchEnabled ? "#222222" : "transparent"
                            }
                        }
                    onClicked: {
                        m.searchEnabled = !m.searchEnabled
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

            width: root.width
            height: m.searchEnabled ? 30 : 0

            visible: m.searchEnabled

            color: "transparent"

            function show(){
                m.searchEnabled = true
                searchEdit.forceActiveFocus()
            }

            Behavior on height { PropertyAnimation { easing.type: Easing.InOutQuad ; duration: 100 } }
            Behavior on visible { PropertyAnimation { easing.type: Easing.InOutQuad ; duration: 50 } }

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
                        placeholderText: "Search ..."

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
                            root.model.loadData(text.trim())
                        }

                        onFocusChanged: {
                            if(!focus)
                                m.searchEnabled = false
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

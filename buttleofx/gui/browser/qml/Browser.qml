import QtQuick 2.1
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0

import "../../../gui"

Rectangle {
	id: browser
    color: "#353535"

    signal buttonCloseClicked(bool clicked)
    signal buttonFullscreenClicked(bool clicked)

    QtObject {
        id: m
        property string directory: "/"
        property string filepath: ""
        property string fileFolder: "/"
        property string fileType: ""
        property real fileSize
        property string filter:"*"
        property variant selected
    }

    ListModel {
        id: listPrevious
    }

    focus: true

    Tab {
        id: tabBar
        name: "Browser"
        onCloseClicked: browser.buttonCloseClicked(true)
        onFullscreenClicked: browser.buttonFullscreenClicked(true)
    }


    ColumnLayout {
        anchors.fill: parent
        anchors.topMargin: tabBar.height

	    HeaderBar {
            id: headerBar
            y: tabBar.height
            Layout.fillWidth: true
            Layout.preferredHeight: 40

           	z: files.z + 1

            listPrevious: listPrevious
            parentFolder: m.fileFolder
            folder: m.directory
            onChangeFolder: {
                m.directory = folder
            }
	    }

        CheckBox {
	    	id: check
            text: "List"
        }

        SplitView {
	        Layout.fillWidth: true
	        Layout.fillHeight: true
            orientation: Qt.Horizontal

		    WindowFiles {
			    id: files
                Layout.fillWidth: true
	            Layout.fillHeight: true
                Layout.preferredHeight: 120
                z: 1
			    
                viewList: check.checked
                folder: m.directory
                onGoToFolder: {
                    listPrevious.append({"url": m.directory})
                    m.directory= newFolder
                }
                filterName: m.filter
                onChangeFile: {
                    m.filepath = file
                }
                onChangeFileFolder: {
                    m.fileFolder = fileFolder
                }
                onChangeFileSize: {
                    m.fileSize = fileSize
                }

                onChangeFileType: {
                    m.fileType = fileType
                }
                onChangeSelectedList: {
                    m.selected = selected
                }
		    }

	    }

	    FooterBar {
		    id: footerBar
            Layout.fillWidth: true
            Layout.preferredHeight: 40

            selected: m.selected
            fileName: m.filepath
            fileType : m.fileType
            fileSize: m.fileSize / 1024
            onChangeFilter: {
                m.filter = newFilter
            }
            onOpenFolder: {
                listPrevious.append({"url": m.directory})
                m.directory = newFolder
            }
	    }

    }


    Keys.onPressed: {
        if ((event.key == Qt.Key_L) && (event.modifiers & Qt.ControlModifier)) {
            headerBar.forceActiveFocusOnPath()
            event.accepted = true
        }
        if ((event.key == Qt.Key_N) && (event.modifiers & Qt.ControlModifier)) {
            files.forceActiveFocusOnCreate()
            event.accepted = true
        }
        if (event.key == Qt.Key_F2) {
            files.forceActiveFocusOnRename()
            event.accepted = true
        }
        if (event.key == Qt.Key_Delete){
            files.forceActiveFocusOnDelete()
            event.accepted = true
        }
    }

}


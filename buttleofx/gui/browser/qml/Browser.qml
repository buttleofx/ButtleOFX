import QtQuick 2.1
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0

import "../../../gui"

Rectangle {
	id: browser
    color: "#353535"

    signal buttonCloseClicked(bool clicked)

    QtObject {
        id: m
        property string directory: "/"
        property string filepath: ""
        property string fileFolder: "/"
        property string fileType: ""
        property string filter:"*"
    }


    Tab {
        id: tabBar
        name: "Browser"
        onCloseClicked: browser.buttonCloseClicked(true)
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

            parentFolder: m.fileFolder
            folder: m.directory
            onChangeFolder: {
                m.directory = folder
                console.debug("folder has changed to " + folder)
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
			    
                viewGrid: check.checked
                folder: m.directory
                onGoToFolder: {
                    console.debug("folder has changed to " + newFolder)
                    m.directory= newFolder
                }
                filterName: m.filter
                onChangeFile: {
                    m.filepath = file
                    console.debug("filepath has changed to " + m.filepath)
                }
                onChangeFileFolder: {
                    m.fileFolder = fileFolder
                    console.debug("fileFolder has changed to " + m.fileFolder)
                }

                onChangeFileType: {
                    m.fileType = fileType
                    console.debug("fileType has changed to " + m.fileType)
                }
		    }

	    }

	    FooterBar {
		    id: footerBar
            Layout.fillWidth: true
            Layout.preferredHeight: 40

            fileName: m.filepath
            fileType : m.fileType
            onChangeFilter: {
                console.debug("filter has changed to " + newFilter)
                m.filter = newFilter
            }
            onOpenFolder: {
                console.debug("folder has changed to " + newFolder)
                m.directory = newFolder
            }
	    }

    }
}


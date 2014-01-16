import QtQuick 2.1
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0

import "../../../gui"

Rectangle {
	id: browser
    color: "#353535"

    QtObject {
        id: m
        property string directory: "/"
        property string filepath: ""
        property string fileFolder: "/"
        property string fileType: ""
        property string filter:"*"
    }



    ColumnLayout {
	    anchors.fill: parent

        Tab {
            id: tabBar
            name: "Browser"
        }

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

        /*CheckBox {
	    	id: check
	    	text: "Viewer"
        }*/

        SplitView {
	        Layout.fillWidth: true
	        Layout.fillHeight: true
            orientation: Qt.Horizontal

            /*LeftCol {
                id: left
                Layout.minimumWidth: 80
                Layout.preferredWidth: 150
	            Layout.fillHeight: true
            }*/

		    WindowFiles {
			    id: files
		        Layout.fillWidth: true
	            Layout.fillHeight: true
                Layout.preferredHeight: 120
                z: 1
			    
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

            /*Viewer {
		    	id: viewer

                Layout.fillWidth: check.checked
                Layout.fillHeight: true

                Layout.preferredWidth: 1

                filepath: m.filepath
            }*/
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


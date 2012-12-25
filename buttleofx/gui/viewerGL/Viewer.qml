import QtQuick 1.1
import Viewport 1.0

Rectangle {
    id: container
    anchors.fill: parent
    implicitWidth: 500
    implicitHeight: 500
    color:"lightblue"

    GLViewport {
        id: viewport
        objectName: "glviewer"

	property real inWidth: 16
	property real inHeight: 9
	property real inRatio: inWidth/inHeight

	property real outWidth: parent.width
	property real outHeight: parent.height
	property real ratioWidth: outWidth / inWidth
	property real ratioHeight: outHeight / inHeight
	property real fitOnWidth: ratioWidth > ratioHeight
        property real fitRatio: fitOnWidth ? ratioWidth : ratioHeight

        anchors.fill: parent

	MouseArea {
		anchors.fill: parent
         	acceptedButtons: Qt.LeftButton | Qt.RightButton
		onClicked: { console.log('onClicked GLViewport QML') }
	}
    }

}



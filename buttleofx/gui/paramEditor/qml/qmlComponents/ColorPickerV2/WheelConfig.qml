pragma Singleton
import QtQuick 2.0

QtObject {
    // Config path
    property string quickmambaPath

    // Style
    // General colors
    property color background: "#333"
    property color accent: "#00B2A1"
    property color border: Qt.darker(background)

    // Text
    property color textColor: "white"
    property string font: "Verdana"
    property int textSize: 15


}

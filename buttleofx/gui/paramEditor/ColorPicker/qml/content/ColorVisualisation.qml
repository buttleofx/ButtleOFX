import QtQuick 2.0
import QtQuick.Layouts 1.1
import "../." // Qt-BUG import qmldir to use config singleton
import "ColorUtils.js" as ColorUtils

RowLayout {
    id: root
    property vector4d colorRGBA

    signal updatedRGBA(var rgba)

    ExposeColor {
        Layout.fillWidth: true
        Layout.fillHeight: true

        colorRGBA: root.colorRGBA
    }

    ExposeColor {
        id: rgbComplementary
        Layout.fillWidth: true
        Layout.fillHeight: true

        colorRGBA: ColorUtils.complementaryColorRGBA(root.colorRGBA)

        MouseArea {
            anchors.fill: parent
            cursorShape: Qt.PointingHandCursor

            onClicked: root.updatedRGBA(rgbComplementary.colorRGBA)
        }
    }
}

import QtQuick 2.0
import QtQuick.Layouts 1.1
import "../." // Qt-BUG import qmldir to use config singleton
import "ColorUtils.js" as ColorUtils

RowLayout {
    id: root
    property vector4d colorRGBA

    signal updatedRGBA(var rgba)
    spacing: 20

    ExposeColor {
        Layout.fillWidth: true
        Layout.fillHeight: true
        colorRGBA: root.colorRGBA
    }

    ColumnLayout {
        Layout.maximumWidth: 500
        Layout.fillHeight: true

        RowLayout
        {
            Layout.fillWidth: true
            Layout.fillHeight: true

            Text {
                text: "RGB Complementary"
                color: Config.textColor
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

        RowLayout
        {
            Layout.fillWidth: true
            Layout.fillHeight: true

            Text {
                text: "RYB Complementary"
                color: Config.textColor
            }

            ExposeColor {
                id: rybComplementary
                Layout.fillWidth: true
                Layout.fillHeight: true

                colorRGBA: {
                    var ryba = ColorUtils.rgba2ryba(root.colorRGBA)
                    var comp = ColorUtils.complementaryColorRGBA(ryba)
                    return ColorUtils.ryba2rgba(comp)
                }

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor

                    onClicked: root.updatedRGBA(rybComplementary.colorRGBA)
                }
            }
        }
    }
}

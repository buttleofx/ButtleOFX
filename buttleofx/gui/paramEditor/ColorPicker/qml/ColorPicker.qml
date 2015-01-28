import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Layouts 1.1
import QuickMamba 1.0
import "content"
import "content/ColorUtils.js" as ColorUtils
import "content/mathUtils.js" as MathUtils
import "." // Qt-BUG import qmldir to use config singleton

Item {
    id: root
    anchors.fill: parent
    anchors.margins: parent.width * 0.01

    // Color value in RGBA with floating point values between 0.0 and 1.0.
    property vector4d colorRGBA: Qt.vector4d(1, 1, 1, 1)
    property bool hasAlpha: true
    property int indexMode: 1

    onColorRGBAChanged: {
        var hsva = ColorUtils.rgba2hsva(root.colorRGBA);
        m.colorHSVA = hsva;
    }

    QtObject {
        id: m
        // Color value in HSVA with floating point values between 0.0 and 1.0.
        // updated when RGBA change
        property vector4d colorHSVA:  Qt.vector4d(0, 0, 1, 1)
    }

    signal accepted
    onAccepted: console.debug("UPDATE TUTLE")

    ColumnLayout {
        anchors.fill: parent

        RowLayout {

            // Display a shape representation as wheel, rainbow...
            ColorRepresentation {
                id:colorRepresentation
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.minimumWidth: 150
                Layout.maximumWidth:  MathUtils.clamp(root.width / 2, 150, Number.POSITIVE_INFINITY)
                Layout.minimumHeight: 150

                colorRGBA: root.colorRGBA
                colorHSVA: m.colorHSVA

                onColorRGBUpdate: root.colorRGBA = ColorUtils.roundColor4D(rgba,  params.precision)

                onColorHSVUpdate: {
                    var rgba = ColorUtils.hsva2rgba(hsva)
                    root.colorRGBA = ColorUtils.roundColor4D(rgba,  params.precision)
                    // When the color is a grey level color, we must conserve the lost hue and saturation by conversion
                    if (ColorUtils.isGreyLvlColor(root.colorRGBA)) {
                        m.colorHSVA.x = hsva.x
                        m.colorHSVA.y = hsva.y
                    }
                }

                onAccepted: root.accepted()
            }

            ColumnLayout
            {
                Layout.fillWidth: true
                Layout.fillHeight: true

                RowLayout {
                    Layout.minimumHeight: 44
                    Layout.maximumHeight: 60
                    Layout.alignment: Layout.Center

                    HexaInput {
                        Layout.fillHeight: true

                        colorRGB: Qt.vector3d(root.colorRGBA.x, root.colorRGBA.y,
                                              root.colorRGBA.z)
                        onUpdatedColor: root.colorRGBA = Qt.vector4d(rgb.x, rgb.y, rgb.z,
                                                                     root.colorRGBA.w)
                    }

                    ScreenPicker {
                        Layout.fillHeight: true
                        onAccepted: root.accepted()
                        onGrabbedColor: {
                            var rgbColor = ColorUtils.hexa2rgb(color)
                            root.colorRGBA = Qt.vector4d(rgbColor.x, rgbColor.y, rgbColor.z, root.colorRGBA.w)
                        }
                    }

                    Rectangle {
                        id: paramsButton
                        border.width: Config.borderWidth
                        border.color: Config.borderColor
                        radius: Config.radius
                        color: Config.backgroundColor
                        Layout.fillHeight: true
                        Layout.minimumWidth: 50

                        MouseArea {
                            anchors.fill: parent
                            hoverEnabled: true
                            onEntered: params.visible = true
                            onExited: params.visible = false
                        }

                        Params
                        {
                            id:params
                            color: Config.windowColor
                            height: 60
                            width: 200
                            anchors.top: paramsButton.bottom
                            anchors.horizontalCenter: paramsButton.horizontalCenter

                            visible: false
                        }
                    }
                }

                // Give tool to edit precisely a color or a channel by text input, slider, picker...
                ChannelsEditor {
                    z: -1
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    colorRGBA: root.colorRGBA
                    colorHSVA: m.colorHSVA
                    precision: params.precision
                    hasAlpha: root.hasAlpha

                    onColorRGBUpdate: root.colorRGBA = ColorUtils.roundColor4D(rgba,  params.precision)

                    onColorHSVUpdate: {
                        var rgba = ColorUtils.hsva2rgba(hsva)
                        root.colorRGBA = ColorUtils.roundColor4D(rgba,  params.precision)
                        // When the color is a grey level color, we must conserve the lost hue and saturation by conversion
                        if (ColorUtils.isGreyLvlColor(root.colorRGBA)) {
                            m.colorHSVA.x = hsva.x
                            m.colorHSVA.y = hsva.y
                        }
                    }
                    onAccepted: root.accepted()
                }
            }
        }

        RowLayout {
            // Display the color choosen and her complementary
            ColorVisualisation {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.minimumHeight: 50
                Layout.minimumWidth: 150
                color: Qt.rgba(root.colorRGBA.x, root.colorRGBA.y, root.colorRGBA.z, root.colorRGBA.w)
            }
        }
    }

}

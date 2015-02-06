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
        var hsva = ColorUtils.rgba2hsva(root.colorRGBA)
        m.colorHSVA = hsva
    }

    QtObject {
        id: m
        // Color value in HSVA with floating point values between 0.0 and 1.0.
        // updated when RGBA change
        property vector4d colorHSVA:  Qt.vector4d(0, 0, 1, 1)

        function updateByHSVA(hsva) {
            var rgba = ColorUtils.hsva2rgba(hsva)
            root.colorRGBA = ColorUtils.roundColor4D(rgba,  params.precision)
            // When the color is a grey level color, we must conserve the lost hue and saturation by conversion
            if (ColorUtils.isGreyLvlColor(root.colorRGBA)) {
                m.colorHSVA.x = hsva.x
                m.colorHSVA.y = hsva.y
            }
            if (hsva.x == 1)
                m.colorHSVA.x = 1
        }
    }

    signal accepted

    ColumnLayout {
        anchors.fill: parent

        RowLayout {

            // Display a shape representation as wheel, rainbow...
            ColorMode {
                id:colorRepresentation
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.minimumWidth: 150
                Layout.maximumWidth:  MathUtils.clamp(root.width / 2, 150, Number.POSITIVE_INFINITY)
                Layout.minimumHeight: 150

                colorRGBA: root.colorRGBA
                colorHSVA: m.colorHSVA

                onColorRGBUpdate: root.colorRGBA = ColorUtils.roundColor4D(rgba,  params.precision)

                onColorHSVUpdate: m.updateByHSVA(hsva)

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
                    spacing: 15

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
                        Layout.minimumWidth: 60

                        function paramsHover() {
                            params.visible = true
                            paramsIcon.source = "img/gearHover.png"
                        }

                        function paramsExit() {
                            params.visible = false
                            paramsIcon.source = "img/gear.png"
                        }

                        Image {
                            id: paramsIcon
                            anchors.centerIn: parent
                            source: "img/gear.png"
                        }

                        MouseArea {
                            anchors.fill: parent
                            hoverEnabled: true
                            onEntered:  paramsButton.paramsHover()
                            onExited: paramsButton.paramsExit()
                        }

                        Params
                        {
                            id:params
                            color: Config.windowColor
                            height: 120
                            width: 200
                            anchors.top: paramsButton.bottom
                            anchors.topMargin: -5
                            anchors.horizontalCenter: paramsButton.horizontalCenter

                            visible: false
                            onEntered:  paramsButton.paramsHover()
                            onExited: paramsButton.paramsExit()
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
                    zeroOneInterval: false

                    onColorRGBUpdate: root.colorRGBA = ColorUtils.roundColor4D(rgba,  params.precision)

                    onColorHSVUpdate: m.updateByHSVA(hsva)
                    onAccepted: root.accepted()
                }
            }
        }

        // Display the color choosen and her complementary
        ColorExpose {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.minimumHeight: 50
            Layout.minimumWidth: 150

            colorRGBA: root.colorRGBA
            onUpdatedRGBA: {
                root.colorRGBA = rgba
                root.accepted()
            }
        }

    }

}

import QtQuick 2.0

Item
{
    id: root

    property real value
    // Color for the gradient
    property vector4d fromColor
    property vector4d toColor
    // Or for other special gradient use :
    property alias gradient: gradient.gradient
    // If no gradient alpha alpha is set by opacity because gradient alpha is not stable
    property bool gradientAlpha: false


    signal accepted
    signal updatedValue(var updatedValue)

    Image {
        anchors.fill: parent
        source: "../img/checkerboard.jpg"
        fillMode: Image.Tile
    }

    Rectangle {
        // 4 lines to have a left-right gradient in spite of top - bottom !
        id: gradient
        width: parent.height
        height: parent.width
        anchors.centerIn: parent
        rotation: 90
        opacity: gradientAlpha ? 1 : root.fromColor.w

        gradient: Gradient {

           GradientStop {
               id: brightnessBeginColor
               position: 0.0
               color: Qt.rgba(root.fromColor.x, root.fromColor.y, root.fromColor.z, gradientAlpha ? root.fromColor.w : 1)
           }
           GradientStop {
               position: 1.0
               color: Qt.rgba(root.toColor.x, root.toColor.y, root.toColor.z, gradientAlpha ? root.toColor.w : 1)
           }
        }
    }


    HorizontalSlider
    {
        id: horizontalSlider
        anchors.fill: parent

        value: root.value

        onUpdatedValue: root.updatedValue(horizontalSlider.value)
        onAccepted: root.accepted()
    }
}

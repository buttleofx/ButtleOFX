import QtQuick 2.0

Item
{
    id: root

    property real value
    // Color for the gradient
    property color fromColor
    property color toColor
    // Or for other special gradient use :
    property alias gradient: gradient.gradient


    signal accepted
    signal updatedValue(var updatedValue)



        CheckerBoard {
            anchors.fill: parent
        }

        Rectangle {
            // 4 lines to have a left-right gradient in spite of top - bottom !
            id: gradient
            width: parent.height
            height: parent.width
            anchors.centerIn: parent
            rotation: 90

            gradient: Gradient {

               GradientStop {
                   id: brightnessBeginColor
                   position: 0.0
                   color: fromColor
               }
               GradientStop {
                   position: 1.0
                   color: toColor
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

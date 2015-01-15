import QtQuick 2.0
import QtQuick.Layouts 1.1

RowLayout
{
    id: root

    property real value

    signal updatedValue(var updatedValue)
    signal accepted

    NumberBox {
        id: numberbox
        Layout.fillWidth: true
        Layout.fillHeight: true

        // TODO: put in NumberBox
        value: root.value // 5 Decimals
        decimals: 2
        max: 1
        min: 0
        caption: "H"

        onAccepted: {
            root.updatedValue(updatedValue);
            root.accepted();
        }
    }

    Item
    {
        Layout.fillWidth: true
        Layout.fillHeight: true
        Rectangle {
            // 4 lines to have a left-right gradient in spite of top - bottom !
            width: parent.height
            height: parent.width
            anchors.centerIn: parent
            rotation: 270

            gradient: Gradient {

               GradientStop {
                   position: 0.0
                   color: "#ff0000"
               }
               GradientStop {
                   position: 0.17
                   color: "#ffff00"
               }
               GradientStop {
                   position: 0.34
                   color: "#00ff00"
               }
               GradientStop {
                   position: 0.5
                   color: "#00ffff"
               }
               GradientStop {
                   position: 0.66
                   color: "#0000ff"
               }
               GradientStop {
                   position: 0.82
                   color: "#ff00ff"
               }
               GradientStop {
                   position: 1
                   color: "#ff0000"
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
}

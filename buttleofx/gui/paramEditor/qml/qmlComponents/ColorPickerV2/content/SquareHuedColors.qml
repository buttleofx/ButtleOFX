import QtQuick 2.0
import "ColorUtils.js" as ColorUtils
import "mathUtils.js" as MathUtils

Item {
    id: root

    property vector3d colorHSV

    signal saturationLuminanceChange(var updatedSaturation, var updatedLuminance)
    signal accepted

//    states :
//        State {
//            // When user is moving the slider
//            name: "editing"
//            PropertyChanges {
//                target: root
//                // Initialize with the value in the default state.
//                // Allows to break the link in that state.
//                saturation: saturation
//                luminance: luminance
//            }
//        }

    Rectangle {
        id: squareHued
        anchors.fill: parent

        ShaderEffect {
            id: shader
            anchors.fill: parent
            property real hue: root.colorHSV.x

            vertexShader: "
                uniform highp mat4 qt_Matrix;
                attribute highp vec4 qt_Vertex;
                attribute highp vec2 qt_MultiTexCoord0;
                varying highp vec2 coord;

                float projectValue(float x, float xmin, float xmax, float ymin, float ymax) {
                    return ((x - xmin) * ymax - (x - xmax) * ymin) / (xmax - xmin);
                }

                void main() {
                    coord.x = qt_MultiTexCoord0.x;
                    coord.y = projectValue(qt_MultiTexCoord0.y, 0, 1, 1, 0);
                    gl_Position = qt_Matrix * qt_Vertex;
            }"

            fragmentShader: "
                varying highp vec2 coord;
                uniform float hue;

                vec3 hsv2rgb(in vec3 c){
                    vec4 k = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
                    vec3 p = abs(fract(c.xxx + k.xyz) * 6.0 - k.www);
                    return c.z * mix(k.xxx, clamp(p - k.xxx, 0.0, 1.0), c.y);
                }

                void main() {

                    vec3 hsl = vec3(hue, coord.x, coord.y);
                    vec3 rgb = hsv2rgb(hsl);
                    gl_FragColor.rgb = rgb;
                    gl_FragColor.a = 1.0;
            }"
        }

        Item {
            id: pickerCursor
            x: root.colorHSV.y * parent.width - r
            y: MathUtils.projectValue(root.colorHSV.z, 0, 1, 1, 0) * parent.height - r

            // radius of the cursor
            property int r : 8

            Rectangle {
                width: parent.r*2; height: parent.r*2
                radius: parent.r
                border.color: "black"; border.width: 2
                color: "transparent"
                Rectangle {
                    anchors.fill: parent; anchors.margins: 2;
                    border.color: "white"; border.width: 2
                    radius: width/2
                    color: "transparent"
                }
            }
        }

        MouseArea {
            id : squareHuedArea
            anchors.fill: parent

            // Change to editing state to move the cursor in the squareHued and calcul new hue and luminance
            function modifySaturationLuminance(mouse) {
//                root.state = 'editing'
                if (mouse.buttons & Qt.LeftButton) {
                    var saturation = MathUtils.clamp(mouse.x / squareHued.width, 0, 1)
                    var luminance = MathUtils.clampAndProject(mouse.y / squareHued.height, 0, 1, 1, 0)

                    root.saturationLuminanceChange(saturation, luminance);
                }
            }

            onPositionChanged: modifySaturationLuminance(mouse)
            onPressed: modifySaturationLuminance(mouse)
            onReleased: {
//                root.state = '';
                root.accepted();
            }
        }
    }
}

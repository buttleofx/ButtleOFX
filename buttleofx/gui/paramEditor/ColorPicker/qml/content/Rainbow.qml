import QtQuick 2.0
import "ColorUtils.js" as ColorUtils
import "mathUtils.js" as MathUtils

Item {
    id: root

    property real hue: 1
    property real luminance: 1

    signal hueLuminanceChange(var updatedHue, var updatedLuminance)
    signal accepted

    Rectangle {
        id: rainbow
        anchors.fill: parent

        ShaderEffect {
            id: shader
            anchors.fill: parent

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

                vec3 hsv2rgb(in vec3 c){
                    vec4 k = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
                    vec3 p = abs(fract(c.xxx + k.xyz) * 6.0 - k.www);
                    return c.z * mix(k.xxx, clamp(p - k.xxx, 0.0, 1.0), c.y);
                }

                void main() {

                    vec3 hsl = vec3(coord.x, 1, coord.y);
                    vec3 rgb = hsv2rgb(hsl);
                    gl_FragColor.rgb = rgb;
                    gl_FragColor.a = 1.0;
            }"
        }

        Item {
            id: pickerCursor
            x: root.hue * parent.width - r
            y: MathUtils.projectValue(root.luminance, 0, 1, 1, 0) * parent.height - r

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
            id : rainbowArea
            anchors.fill: parent

            // Change to editing state to move the cursor in the rainbow and calcul new hue and luminance
            function modifyHueLuminance(mouse) {
                if (mouse.buttons & Qt.LeftButton) {
                    var hue = MathUtils.clamp(mouse.x / rainbow.width, 0, 1)
                    var luminance = MathUtils.clampAndProject(mouse.y / rainbow.height, 0, 1, 1, 0)

                    root.hueLuminanceChange(hue, luminance);
                }
            }

            onPositionChanged: modifyHueLuminance(mouse)
            onPressed: modifyHueLuminance(mouse)
            onReleased: root.accepted()
        }
    }
}

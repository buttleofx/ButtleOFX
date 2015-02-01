import QtQuick 2.0
import "mathUtils.js" as MathUtils

Item {
    id: root

    property real hue: 1
    property real saturation: 1
    property int precision: 5

    signal accepted
    signal hueSaturationChange(var updatedHue, var updatedSaturation)

    Rectangle {
        id: wheel

        //Keep the wheel round
        width: parent.width < parent.height ? parent.width : parent.height ;
        height: width ;
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        color: "transparent"

        ShaderEffect {
            id: shader
            anchors.fill: parent

            vertexShader: "
                uniform highp mat4 qt_Matrix;
                attribute highp vec4 qt_Vertex;
                attribute highp vec2 qt_MultiTexCoord0;
                varying highp vec2 coord;

                void main() {
                    coord = qt_MultiTexCoord0 - vec2(0.5, 0.5);
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
                    const float PI = 3.14159265358979323846264;
                    float s = sqrt(coord.x * coord.x + coord.y * coord.y);

                    if( s > 0.5 ){
                        gl_FragColor = vec4(0, 0, 0, 0);
                        return;
                    }

                    float h = - atan( coord.y / coord.x );
                    s *= 2.0;

                    if( coord.x >= 0.0 ){
                        h += PI;
                    }

                    h = h / (2.0 * PI);
                    vec3 hsl = vec3(h, s, 1.0);
                    vec3 rgb = hsv2rgb(hsl);
                    gl_FragColor.rgb = rgb;
                    gl_FragColor.a = 1.0;
            }"
        }

        Item {
            id: pickerCursor
            x: parent.width/2 * (1 + root.saturation * Math.cos(2 * Math.PI * root.hue - Math.PI)) - r
            y: parent.width/2 * (1 + root.saturation * Math.sin(-2 * Math.PI * root.hue - Math.PI)) - r

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
            id : wheelArea
            anchors.fill: parent

            // Change to editing state to move the cursor in the wheel and calcul new hue and saturation
            function modifyHueSaturation(mouse, wheelArea, wheel) {
                if (mouse.buttons & Qt.LeftButton) {
                    // cartesian to polar coords
                    var ro = Math.sqrt(Math.pow(mouse.x-wheel.width/2,2)+Math.pow(mouse.y-wheel.height/2,2));
                    var theta = Math.atan2(((mouse.y-wheel.height/2)*(-1)),((mouse.x-wheel.width/2)));

                    // Wheel limit
                    if(ro > wheel.width/2)
                        ro = wheel.width/2;

                    // polar to cartesian coords
                    var cursor = Qt.vector2d(0, 0);
                    cursor.x = Math.max(-pickerCursor.r, Math.min(wheelArea.width, ro*Math.cos(theta)+wheel.width/2)-pickerCursor.r);
                    cursor.y = Math.max(-pickerCursor.r, Math.min(wheelArea.height, wheel.height/2-ro*Math.sin(theta)-pickerCursor.r));

                    var hue = MathUtils.decimalRound(Math.atan2(((cursor.y+pickerCursor.r-wheel.height/2)*(-1)),((cursor.x+pickerCursor.r-wheel.width/2)))/(Math.PI*2)+0.5, root.precision)
                    var saturation = MathUtils.decimalRound(Math.sqrt(Math.pow(cursor.x+pickerCursor.r-width/2,2)+Math.pow(cursor.y+pickerCursor.r-height/2,2))/wheel.height*2, root.precision);

                    root.hueSaturationChange(hue, saturation);
                }
            }

            onPositionChanged: modifyHueSaturation(mouse, wheelArea,  wheel)
            onPressed: modifyHueSaturation(mouse, wheelArea, wheel)
            onReleased: root.accepted()
        }
    }

}

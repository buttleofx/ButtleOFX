import QtQuick 2.0

Item {
    id: root

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
    }
}

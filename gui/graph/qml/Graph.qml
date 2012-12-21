import QtQuick 1.1

Rectangle {
    y: 30
    implicitWidth: 850
    implicitHeight: 350 - y
    z: 0
    gradient: Gradient {
        GradientStop { position: 0.0; color: "#111111" }
        GradientStop { position: 0.015; color: "#212121" }
    }
    Repeater {
        model : _wrappers
        Node {}
    }
}

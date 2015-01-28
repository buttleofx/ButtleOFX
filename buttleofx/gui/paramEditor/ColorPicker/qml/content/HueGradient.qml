import QtQuick 2.0

Gradient {
    id:root
    property real opacity: 1

    GradientStop {
        position: 0
        color: Qt.rgba(1, 0, 0, root.opacity)
    }
    GradientStop {
        position: 0.17
        color: Qt.rgba(1, 0, 1, root.opacity)
    }
    GradientStop {
        position: 0.34
        color: Qt.rgba(0, 0, 1, root.opacity)
    }
    GradientStop {
        position: 0.5
        color: Qt.rgba(0, 1, 1, root.opacity)
    }
    GradientStop {
        position: 0.66
        color: Qt.rgba(0, 1, 0, root.opacity)
    }
    GradientStop {
        position: 0.82
        color: Qt.rgba(1, 1, 0, root.opacity)
    }
    GradientStop {
        position: 1
        color: Qt.rgba(1, 0, 0, root.opacity)
    }
}

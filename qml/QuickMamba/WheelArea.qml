import QtQuick 2.0
import QuickMamba 1.0

WheelAreaImpl {
    id: wheelArea
    anchors.fill: parent
    
    // HACK to expose signal parameters with named params
    signal verticalWheel(variant pos, int delta, variant buttons, variant modifiers)
    signal horizontalWheel(variant pos, int delta, variant buttons, variant modifiers)
    
    Component.onCompleted: {
        wheelArea.internVerticalWheel.connect(verticalWheel)
        wheelArea.internHorizontalWheel.connect(horizontalWheel)
    }
}



import QtQuick 2.0

Rectangle {
    id:root
    width: 1
    opacity: 1
    color: "#00B2A1"

    property real blinkInterval: 500

    Timer {
         id: timerDisappear
         interval: root.blinkInterval
         running: true
         onTriggered:   {
             root.opacity = 0
             timerAppear.start()
        }

     }
     Timer {
          id: timerAppear
          interval: root.blinkInterval
          onTriggered: {
              root.opacity = 1
              timerDisappear.restart()
        }
    }
}

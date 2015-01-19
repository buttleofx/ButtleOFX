import QtQuick 2.2
import QtQuick.Layouts 1.1

TextInput {
    id: textInput
    selectByMouse: true

    signal quickUpdate(var text)

    // stepSign is the factor of step (eg: 1 will increment, -1 will decrement)
    function updateValue(stepSign) {
        stepSign = typeof stepSign !== 'undefined' ? stepSign : 1

        // Remember cursor position to stay in same place after text update (because we lose it when property text changes)
        var oldCursorPos = textInput.cursorPosition

        var text =  textInput.text
        var comaPosition = text.indexOf(".")

        var step = 1
        // Calcul step in function of cursor position if the value is integer, if cursor is before sign - step is just 1
        if(!(parseFloat(textInput.text) < 0 && oldCursorPos == 0))
        {
            if(comaPosition == -1)
                step = Math.pow(10, text.length - oldCursorPos - 1)
            else if(oldCursorPos < comaPosition)
                step = Math.pow(10, comaPosition - oldCursorPos - 1)
            else if (oldCursorPos > comaPosition)
                step = Math.pow(10, comaPosition - oldCursorPos)
        }

        var newValue = parseFloat(textInput.text) + stepSign * step
        // Fix problem when changing sign, we must correct cursor position
        if (newValue >= 0 && parseFloat(textInput.text) < 0)
            oldCursorPos--

        quickUpdate(newValue)

        textInput.cursorPosition = oldCursorPos
    }

    QtObject {
        id: m
        property string textUpdated
    }

    Keys.onPressed: {
        switch(event.key) {
            case Qt.Key_Up :
                updateValue(1)
                event.accepted = true
                break
            case Qt.Key_Down :
                updateValue(-1)
                event.accepted = true
                break
        }
    }
}

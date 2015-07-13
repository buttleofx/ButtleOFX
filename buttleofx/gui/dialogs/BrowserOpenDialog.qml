import QtQuick 2.0

BrowserDialog{
    id: root
    title: 'Open Graph'

    Connections{
        target: root.browser.fileWindow
        onItemDoubleClicked:{
            if (!isFolder && absolutePath != "") {
                _buttleData.loadData(absolutePath)
                root.visible = false
            }
        }
    }
}

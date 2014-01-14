import QtQuick 2.0
import QtQuick.Dialogs 1.0

FileDialog {
    id: finderLoadGraph
    title: "Open a graph"
    folder: _buttleData.buttlePath
    nameFilters: [ "ButtleOFX Graph files (*.bofx)", "All files (*)" ]
    selectedNameFilter: "All files (*)"
    onAccepted: {
        console.log(finderLoadGraph.fileUrl)
        _buttleData.loadData(finderLoadGraph.fileUrl)
    }
}

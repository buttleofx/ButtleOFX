import QtQuick 2.0
import QtQuick.Dialogs 1.0

FileDialog {
    id: finderSaveGraph
    title: "Save the graph"
    folder: _buttleData.buttlePath
    nameFilters: [ "ButtleOFX Graph files (*.bofx)", "All files (*)" ]
    selectedNameFilter: "All files (*)"
    onAccepted: _buttleData.saveData(finderSaveGraph.fileUrl)
    selectExisting: false
}

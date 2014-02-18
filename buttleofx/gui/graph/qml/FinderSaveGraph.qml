import QtQuick 2.0
import QtQuick.Dialogs 1.0

FileDialog {
    signal getFileUrl(string fileurl)

    id: finderSaveGraph
    title: "Save the graph"
    folder: _buttleData.buttlePath
    nameFilters: [ "ButtleOFX Graph files (*.bofx)", "All files (*)" ]
    selectedNameFilter: "All files (*)"
    onAccepted: {
        _buttleData.saveData(finderSaveGraph.fileUrl)
        getFileUrl(finderSaveGraph.fileUrl)
    }
    selectExisting: false
}

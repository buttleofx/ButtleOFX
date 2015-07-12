import QtQuick 2.2
import QtQuick.Layouts 1.1
import QtQml 2.1
import QtQuick 2.0
import QtQuick.Window 2.1
import QtQuick.Dialogs 1.1
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0


import "../browser_v2/qml/"

// common part of open and save browserDialog (Abstract behavior)
// the connecitons are done in 'subclasses'

Window{
    id: finderBrowser
    title: 'Finder Browser'
    width: 630
    height: 380
    visible: false
    flags: "Dialog"
    modality: "ApplicationModal"
    property alias browser: browser
    property bool showTab: false

    Browser {
        id: browser
        bModel: _browserDialog
        bAction: _browserActionDialog
        anchors.fill: parent
        showTab: finderBrowser.showTab
    }
    onVisibleChanged:{
        if(visible == false)
            browser.bModel.stopLoading()
        else
            browser.navBar.toggleUrlEdit(true)
    }
}

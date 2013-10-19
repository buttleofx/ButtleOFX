import QtQuick 2.0
import QuickMamba 1.0

ExternDropAreaImpl {
    id: externDropAreaItem
    anchors.fill: parent
    
    // HACK to expose signal parameters with named params
    signal dragEnter(
        bool hasText, string text,
        bool hasHtml, string html,
        bool hasUrls, string firstUrl,
        variant buttons, variant dropAction,
        variant modifiers, variant pos,
        variant possibleActions, variant proposedAction,
        string source)
        
    signal dragMove(
        bool hasText, string text,
        bool hasHtml, string html,
        bool hasUrls, string firstUrl,
        variant buttons, variant dropAction,
        variant modifiers, variant pos,
        variant possibleActions, variant proposedAction,
        string source)
        
    signal dragLeave(
        bool hasText, string text,
        bool hasHtml, string html,
        bool hasUrls, string firstUrl,
        variant buttons, variant dropAction,
        variant modifiers, variant pos,
        variant possibleActions, variant proposedAction,
        string source)
        
    signal drop(
        bool hasText, string text,
        bool hasHtml, string html,
        bool hasUrls, string firstUrl,
        variant buttons, variant dropAction,
        variant modifiers, variant pos,
        variant possibleActions, variant proposedAction,
        string source)
    
    Component.onCompleted: {
        externDropAreaItem.internDragEnter.connect(dragEnter)
        externDropAreaItem.internDragMove.connect(dragMove)
        externDropAreaItem.internDragLeave.connect(dragLeave)
        externDropAreaItem.internDrop.connect(drop)
    }
}



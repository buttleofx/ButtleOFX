import QtQuick 1.1

Item {
    id: slider
    implicitWidth : 300
    implicitHeight : 30

    SliderParam {
        paramObject: model.object
    }
}

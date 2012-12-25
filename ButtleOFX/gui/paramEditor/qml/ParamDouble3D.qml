import QtQuick 1.1

/*ParamDouble3D containts three input field*/

/*Container of the three input field*/
Rectangle{
	id: paramDouble3D
    width: 90
    height: 70
    color: "#999999"
    border.width: 1
    border.color: "#111111"
    radius: 4

    Column {
        id: groupeDouble3D
        spacing: 5
        ParamDouble{}
        ParamDouble{}
        ParamDouble{}
    }
}
import QtQuick 1.1

/*ParamDouble2D containts two input field*/

/*Container of the two input field*/
Rectangle{
	id: paramDouble2D
    width: 90
    height: 45
    color: "#999999"
    border.width: 1
    border.color: "#111111"
    radius: 4

    Column {
        id: groupeDouble2D
        spacing: 5
        ParamDouble{}
        ParamDouble{}
    }
}
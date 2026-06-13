import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: card
    width: 200
    height: 120
    radius: 10
    color: "#1a1a2e"
    border.color: status == "active" ? "#00ffff" : "#333"
    border.width: 2
    
    property string agentName: "Agente"
    property string status: "idle"
    
    Column {
        anchors.centerIn: parent
        spacing: 8
        Text {
            text: agentName
            color: "white"
            font.pixelSize: 16
            font.bold: true
            anchors.horizontalCenter: parent.horizontalCenter
        }
        Rectangle {
            width: 10
            height: 10
            radius: 5
            color: status == "active" ? "#00ff00" : (status == "error" ? "#ff0000" : "#888888")
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }
    
    MouseArea {
        anchors.fill: parent
        onClicked: console.log(agentName + " clicked")
    }
}
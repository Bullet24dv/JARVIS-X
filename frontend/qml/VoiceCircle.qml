import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: voiceCircle
    width: 100
    height: 100
    radius: 50
    color: "#00ffff"
    opacity: 0.6
    
    property bool isSpeaking: false
    
    SequentialAnimation on scale {
        running: isSpeaking
        loops: Animation.Infinite
        NumberAnimation { to: 1.2; duration: 300 }
        NumberAnimation { to: 1.0; duration: 300 }
    }
}
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15

Item {
    id: hologram
    width: parent.width
    height: parent.height
    
    property real pulseValue: 0
    property real rotationAngle: 0
    
    Timer {
        interval: 30
        running: true
        repeat: true
        onTriggered: {
            pulseValue += 0.03
            if (pulseValue > 1) pulseValue = 0
            rotationAngle += 2
        }
    }
    
    Rectangle {
        id: coreGlow
        width: 300
        height: 300
        radius: width/2
        color: "#00ffff"
        opacity: 0.3 + Math.sin(pulseValue * Math.PI * 2) * 0.2
        anchors.centerIn: parent
        layer.enabled: true
        layer.effect: Glow {
            radius: 20
            samples: 40
            color: "cyan"
        }
    }
    
    Repeater {
        model: 4
        Rectangle {
            width: 150 + index * 80
            height: width
            radius: width/2
            border.color: "#00ffff"
            border.width: 2
            color: "transparent"
            anchors.centerIn: parent
            rotation: rotationAngle * (index + 1)
            opacity: 0.6 - index * 0.1
        }
    }
    
    Repeater {
        model: 100
        Rectangle {
            width: 4
            height: 4
            radius: 2
            color: "#00ffff"
            opacity: Math.random() * 0.8
            x: parent.width * Math.random()
            y: parent.height * Math.random()
            PropertyAnimation on y {
                duration: 2000 + Math.random() * 3000
                from: parent.height
                to: 0
                loops: Animation.Infinite
                running: true
            }
        }
    }
}
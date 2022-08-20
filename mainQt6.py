#!/usr/bin/env python3

import sys
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QPixmap, QGuiApplication, QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QMenu, QApplication, QWidget, QLabel, QMessageBox
from PyQt6.QtMultimedia import QSoundEffect, QAudioOutput, QMediaPlayer


class TomatoTimer(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.initVars()
        self.initUI()
        self.actions()

    def actions(self):
        # https://doc.qt.io/qt-6/qt.html#Key-enum
        exitAct = QAction(self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(self.close)

    def initVars(self):
        self.logo = 'logo.png'
        self.windowTitle = 'Tomato Timer'
        self.alarmSound = 'sounds/household_alarm_clock_old_fashioned_ring_long.mp3'
        self.click = 'sounds/technology_studio_speaker_active_power_switch_click.mp3'

        self.last_image = 0
        self.volume = 50

    def initUI(self):
        self.setWindowIcon(QIcon(self.logo))
        self.setWindowTitle(self.windowTitle)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.showImage(self.last_image)

        self.timer = QTimer()
        self.timer.timeout.connect(self.countdown)

        
        self.player = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.player.setAudioOutput(self.audioOutput)
        self.audioOutput.setVolume(self.volume)
        
        self.center()

        self.oldPos = self.pos()
        
        self.show()

    

    def playSound(self, audioFile):
        self.player.setSource(QUrl.fromLocalFile(audioFile))
        self.player.play()

    def timerEvent(self, event):
        if self.last_image == 0:
            self.timer.stop()
            return

        self.last_image -= 1
        self.check()
        self.updateImage()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, self.windowTitle, "Are you sure to quit?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

    def wheelEvent(self, event):
        # https://stackoverflow.com/questions/20123935/pyqt-wheel-event
        delta = event.angleDelta().y()
        delta = delta and delta // abs(delta)
        print(self.last_image, delta)
        if not self.timer.isActive():
            self.last_image += delta
            self.check()
            self.updateImage()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPosition().toPoint()
        # https://doc-snapshots.qt.io/qt6-6.2/qmediaplayer.html#PlaybackState-enum
        if self.player.playbackState() == self.player.playbackState().PlayingState:
            self.player.stop()

    def mouseMoveEvent(self, event):
        self.move(self.pos() + event.globalPosition().toPoint() - self.oldPos)
        self.oldPos = event.globalPosition().toPoint()
        event.accept()

    def contextMenuEvent(self, event):
        cmenu = QMenu(self)

        if self.timer.isActive():
            startstopAct = cmenu.addAction("Stop")
        else:            
            startstopAct = cmenu.addAction("Start")

        aboutAct = cmenu.addAction("About")
        quitAct = cmenu.addAction("Quit")
        action = cmenu.exec(self.mapToGlobal(event.pos()))

        if action == quitAct:
            QApplication.instance().quit()
        elif action == startstopAct:
            self.doAction()
        elif action == aboutAct:
            self.showAbout()

    def keyPressEvent(self, event):        
        if event.key() == Qt.Key.Key_Q.value:
            self.close()
        elif event.key() == Qt.Key.Key_Return.value:
            self.doAction()            

    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(1000)

    def countdown(self):
        if self.last_image > 0:
            self.last_image -= 1
            self.check()
            self.updateImage()
        else:
            self.timer.stop()
            self.playSound(self.alarmSound)

    def showAbout(self):
       QMessageBox.information(self, self.windowTitle, 'Written by KMT\n\n\nnew line')

    def check(self):
        if self.last_image > 59:
            self.last_image = self.last_image - 60
        elif self.last_image < 0:
            self.last_image = self.last_image + 60

    def showImage(self, number):
        self.image = QPixmap(self.imageName(number))
        
        self.label_image = QLabel(self)
        self.label_image.setPixmap(self.image)
        self.label_image.setGeometry(0, 0, self.image.width(), self.image.height())

        self.resize(self.image.width(), self.image.height())
        self.label_image.show()

    def updateImage(self):
        self.label_image.clear()
        self.playSound(self.click)
        self.showImage(self.last_image)

    def imageName(self, number):
        number = str(number)
        n = len(number)
        return "images/{}.png".format('0' * (4 - n) + number)

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TomatoTimer()
    sys.exit(app.exec())

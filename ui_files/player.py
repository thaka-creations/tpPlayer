import os
import sys
import random

import utils
import key_utils
from threading import Thread

from PyQt5.QtCore import Qt, QDir, pyqtSignal, QSizeF, QRect, QSize, QBuffer, QIODevice, QSettings
from PyQt5.QtGui import QMovie, QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem
from PyQt5.QtWidgets import QWidget, QPushButton, QStyle, QSlider, QHBoxLayout, QVBoxLayout, \
    QGraphicsScene, QFileDialog, QGraphicsView, QFrame, QLabel, QGraphicsProxyWidget, QMessageBox, QGraphicsTextItem


class VideoWindow(QWidget):
    fullScreenSignal = pyqtSignal()
    errorHandler = pyqtSignal()

    def __init__(self, stackedWidget):
        super().__init__()
        self.stackedWidget = stackedWidget
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.showMaximized()
        self.player = QMediaPlayer(None)
        self.buffer = QBuffer()

        # initialize variables
        self.displayAt = False
        self.fileName = None
        self.secondScreen = None
        self.watermark = None
        self.expiresAt = None
        self.errorList = []
        self.videoList = None
        self.definedWidth = 0
        self.definedHeight = 0
        self.keyPosition = 0
        self.step = 0

        # control buttons
        self.playPauseButton = QPushButton()
        self.playPauseButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.playPauseButton.clicked.connect(self.playPause)
        self.playPauseButton.setFixedSize(50, 50)
        self.playPauseButton.setEnabled(False)

        # stop
        self.stopButton = QPushButton()
        self.stopButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaStop))
        self.stopButton.clicked.connect(self.player.stop)
        self.stopButton.setFixedSize(50, 50)
        self.stopButton.setEnabled(False)

        # forward button
        self.forwardButton = QPushButton()
        self.forwardButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSeekForward))
        self.forwardButton.clicked.connect(self.forward)
        self.forwardButton.setFixedSize(50, 50)
        self.forwardButton.setEnabled(False)

        # backward button
        self.backwardButton = QPushButton()
        self.backwardButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSeekBackward))
        self.backwardButton.clicked.connect(self.backward)
        self.backwardButton.setFixedSize(50, 50)
        self.backwardButton.setEnabled(False)

        # mute button
        self.muteButton = QPushButton()
        self.muteButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolume))
        self.muteButton.clicked.connect(self.mute)
        self.muteButton.setFixedSize(50, 50)
        self.muteButton.setEnabled(False)

        # volume slider
        self.volumeSlider = QSlider(Qt.Orientation.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(100)
        self.volumeSlider.valueChanged.connect(self.player.setVolume)

        # open file button
        self.openFileButton = QPushButton(" Open File")
        self.openFileButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon))
        self.openFileButton.clicked.connect(self.openFile)
        self.openFileButton.setFixedSize(180, 50)

        # close button
        self.closeButton = QPushButton()
        self.closeButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCloseButton))
        self.closeButton.clicked.connect(self.exitPlayer)
        self.closeButton.setFixedSize(50, 50)

        # full screen button
        self.fullScreenButton = QPushButton(" Full Screen")
        self.fullScreenButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarMaxButton))
        self.fullScreenButton.clicked.connect(self.fullScreen)
        self.fullScreenButton.setFixedSize(180, 50)

        # position slider
        self.positionSlider = QSlider(Qt.Orientation.Horizontal)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.positionSlider.setEnabled(False)
        self.positionSlider.setRange(0, 0)

        # create control layout
        self.controlLayout = QHBoxLayout()
        self.controlLayout.addWidget(self.openFileButton)
        self.controlLayout.addWidget(self.backwardButton)
        self.controlLayout.addWidget(self.playPauseButton)
        self.controlLayout.addWidget(self.forwardButton)
        self.controlLayout.addWidget(self.stopButton)
        self.controlLayout.setContentsMargins(5, 0, 5, 0)

        # add spacer
        self.controlLayout.addStretch(1)
        self.controlLayout.addWidget(self.muteButton)
        self.controlLayout.addWidget(self.volumeSlider)
        self.controlLayout.addWidget(self.fullScreenButton)
        self.controlLayout.addWidget(self.closeButton)

        # add position slider to control layout 2
        self.controlLayout2 = QHBoxLayout()
        self.controlLayout2.addWidget(self.positionSlider)
        self.controlLayout2.setContentsMargins(5, 0, 5, 0)

        # spinner
        self.spinner = QLabel()
        self.spinner.setGeometry(QRect(25, 25, 200, 200))
        self.spinner.setMinimumSize(QSize(250, 250))
        self.spinner.setMaximumSize(QSize(250, 250))
        self.spinner.setObjectName("lb1")
        try:
            loader = os.path.join(sys._MEIPASS, "/assets/loader.gif")
        except AttributeError:
            loader = "assets/loader.gif"
        self.movie = QMovie(loader)
        self.spinner.setMovie(self.movie)
        self.spinner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinner.setStyleSheet("background-color: black;")

        self.proxy = QGraphicsProxyWidget()
        self.proxy.setWidget(self.spinner)

        # add video widget to main layout
        self.videoItem = QGraphicsVideoItem()
        self.scene = QGraphicsScene()
        self.scene.addItem(self.videoItem)
        self.scene.installEventFilter(self)
        self.scene.setBackgroundBrush(Qt.GlobalColor.black)
        self.graphicsView = QGraphicsView(self.scene)
        self.graphicsView.setMouseTracking(True)
        self.graphicsView.setFrameShape(QFrame.Shape.NoFrame)
        self.graphicsView.setContentsMargins(0, 0, 0, 0)
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.player.setVideoOutput(self.videoItem)
        self.player.positionChanged.connect(self.positionChanged)
        self.player.durationChanged.connect(self.durationChanged)
        self.player.mediaStatusChanged.connect(self.mediaStatusChanged)
        self.player.error.connect(self.handleError)

        # center video
        self.graphicsView.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # resize event
        self.graphicsView.resizeEvent = self.update_video_widget_size

        # control widget
        self.altLayout = QVBoxLayout()
        self.controlWidget = QWidget()
        self.altLayout.setContentsMargins(0, 0, 0, 10)
        self.altLayout.addLayout(self.controlLayout2)
        self.altLayout.addLayout(self.controlLayout)
        self.controlWidget.setLayout(self.altLayout)
        self.controlWidget.setContentsMargins(0, 0, 0, 0)

        # create main layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.graphicsView)
        self.mainLayout.addWidget(self.controlWidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

        # error handling
        self.errorHandler.connect(self.handleDecryptionError)

        # Set stylesheet
        stylesheet = """
                    QProgressBar {
                        border: 2px solid grey;
                        border-radius: 5px;
                        background-color: white;
                    }
                    QProgressBar::chunk {
                        background-color: blue;
                        width: 10px;
                        margin: 0.5px;
                    }

                    QSlider {
                        background-color: transparent;
                    }

                    QSlider::groove:horizontal {
                        height: 6px;
                        background-color: #d0d0d0;
                        border-radius: 3px;
                    }

                    QSlider::handle:horizontal {
                        width: 16px;
                        height: 16px;
                        background-color: #e5e5e5;
                        border-radius: 8px;
                        margin: -5px 0px;
                    }

                    QSlider::sub-page:horizontal {
                        background-color: #0078d7;
                        border-radius: 2px;
                    }
                    """
        self.setStyleSheet(stylesheet)

    # detect screen change
    def screen_changed(self, value):
        if value:
            self.displayAt = True
        else:
            self.displayAt = False

    # control spinner
    def toggle_spinner(self, state):
        if state:
            self.scene.addItem(self.proxy)
            self.movie.start()
        else:
            self.scene.removeItem(self.proxy)
            self.movie.stop()

    # control layout to hide
    def control_layout_toggle(self, state):
        if state:
            self.controlWidget.setVisible(False)
        else:
            self.controlWidget.setVisible(True)

    # handle decryption error
    def handleDecryptionError(self):
        self.setMedia(self.fileName)

    # update video widget size
    def update_video_widget_size(self, event):
        self.proxy.setPos(self.width() / 2 - 125, self.height() / 2 - 125)
        self.videoItem.setSize(QSizeF(event.size()))
        self.videoItem.update()
        self.graphicsView.update()
        self.graphicsView.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # play pause video
    def playPause(self):
        if self.player.state() == QMediaPlayer.State.PlayingState:
            self.playPauseButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
            self.player.pause()
        else:
            self.playPauseButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
            self.player.play()

    # forward video
    def forward(self):
        if self.player.state() == QMediaPlayer.State.PlayingState:
            self.player.setPosition(self.player.position() + 10000)

    # backward video
    def backward(self):
        if self.player.state() == QMediaPlayer.State.PlayingState:
            self.player.setPosition(self.player.position() - 10000)

    # mute video
    def mute(self):
        if self.player.isMuted():
            self.player.setMuted(False)
            self.muteButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolume))
        else:
            self.player.setMuted(True)
            self.muteButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolumeMuted))

    # remove watermark
    def remove_watermark(self, hide=False):
        if hide:
            # hide watermark on stop
            self.watermark.hide()
        else:
            # remove existing if watermark exists
            if self.watermark in self.scene.items():
                self.scene.removeItem(self.watermark)

    def setPosition(self, position):
        self.player.setPosition(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def set_button_states(self, state):
        self.stopButton.setEnabled(state)
        self.forwardButton.setEnabled(state)
        self.backwardButton.setEnabled(state)
        self.muteButton.setEnabled(state)

    def mediaStatusChanged(self, state):
        if self.player.state() == QMediaPlayer.State.PlayingState:
            self.playPauseButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
        else:
            self.playPauseButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))

    def handleError(self):
        self.playPauseButton.setEnabled(False)
        self.stopButton.setEnabled(False)
        self.positionSlider.setEnabled(False)
        self.playPauseButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))

    def openFile(self):
        # remember home path
        ss = QSettings("TafaPlayer", "TafaPlayer")
        last_dir_abs_path = ss.value("last_dir", QDir.homePath())
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Media", last_dir_abs_path, "Video Files (*.tafa)")
        if file_name != "":
            self.remove_watermark()
            self.keyPosition = 0
            # save last dir in memory to remember video location
            last_dir_abs_path = QDir(file_name).absolutePath()
            ss.setValue("last_dir", last_dir_abs_path)
            self.setMedia(file_name)

    def definedDimensions(self):
        """
        compute boundary watermark positioning
        """
        view_width = self.graphicsView.width()
        view_height = self.graphicsView.height()
        watermark_width = self.watermark.boundingRect().width()
        watermark_height = self.watermark.boundingRect().height()
        x, y = view_width - watermark_width, view_height - watermark_height
        self.definedWidth = x
        self.definedHeight = y

    def addWatermark(self, text):
        """
        adding watermark to graphic scene
        :param text: watermark text
        """
        self.watermark = QGraphicsTextItem(text)
        self.watermark.setFont(QFont("Arial", 20))
        self.watermark.setDefaultTextColor(Qt.GlobalColor.red)
        self.scene.addItem(self.watermark)
        self.definedDimensions()

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

        # move watermark after position has moved twice
        if self.watermark:
            self.step += 1
            if (self.step % 13) == 0:
                x, y = int(self.definedWidth), int(self.definedHeight)
                randX, randY = random.randint(0, x), random.randint(0, y)
                self.watermark.setPos(randX, randY)

    def mediaDecryptor(self, fileName, key, watermark):
        if self.buffer.isOpen():
            self.player.stop()
            self.player.setMedia(QMediaContent(), QBuffer())
            self.buffer.close()

        obj = key_utils.DecryptionTool(fileName, key,
                                       video_list=self.videoList,
                                       expires_at=self.expiresAt,
                                       display_at=self.displayAt,
                                       second_screen=self.secondScreen
                                       )
        content = b''
        for data in obj.decrypt():
            if not data:
                self.keyPosition += 1
                self.errorList = obj.error_list
                self.errorHandler.emit()
                return
            # write to buffer
            content += data

        if bool(watermark):
            self.addWatermark(watermark)

        # set content to buffer
        self.buffer.setData(content)
        self.buffer.open(QIODevice.OpenModeFlag.ReadOnly)
        self.player.setMedia(QMediaContent(), self.buffer)
        self.playPauseButton.setEnabled(True)
        self.set_button_states(True)
        self.positionSlider.setEnabled(True)
        self.toggle_spinner(False)
        self.player.play()

    def retrieveKey(self):
        keys = utils.get_local_keys()
        length_of_keys = len(keys)
        keys.reverse()
        if self.keyPosition > length_of_keys - 1:
            return None
        return keys[self.keyPosition]

    def displayError(self):
        # disable controls
        self.set_button_states(False)

        # remove loader
        self.toggle_spinner(False)
        self.player.stop()

        # display error message
        if 414 in self.errorList:
            error_message = "This video cannot be played on second screen"
        elif 411 in self.errorList:
            error_message = "Kindly purchase this video to play"
        elif 410 in self.errorList:
            error_message = "Your key has expired"
        else:
            error_message = "Invalid key provided"
        self.display_message("Error", error_message)

    def setMedia(self, fileName):
        key = self.retrieveKey()
        if not key:
            self.displayError()
            return
        self.fileName = fileName
        encryption_key = key['encryption_key']
        watermark = key['watermark']
        self.expiresAt = key['expires_at']
        self.secondScreen = key['second_screen']
        self.videoList = key['videos']
        self.scene.addItem(self.proxy)
        self.movie.start()
        Thread(target=self.mediaDecryptor, args=(fileName, encryption_key, watermark),
               daemon=False).start()

    def fullScreen(self):
        self.showFullScreen()
        self.control_layout_toggle(True)
        self.fullScreenSignal.emit()

    def exitPlayer(self):
        self.player.stop()
        self.close()
        self.stackedWidget.setCurrentIndex(0)

    @staticmethod
    def display_message(status_code, message):
        message_box = QMessageBox()
        message_box.setWindowTitle(status_code)
        message_box.setText(message)
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)

        if status_code == "Success":
            message_box.setIcon(QMessageBox.Icon.Information)
        else:
            message_box.setIcon(QMessageBox.Icon.Warning)
        message_box.exec()

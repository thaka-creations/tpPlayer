from PyQt6.QtCore import Qt, QDir, QUrl, pyqtSignal, QSizeF
from PyQt6.QtGui import QCursor, QPainter
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QGraphicsVideoItem
from PyQt6.QtWidgets import QWidget, QApplication, QPushButton, QStyle, QSlider, QHBoxLayout, QVBoxLayout, \
    QGraphicsScene, QFileDialog, QGraphicsView, QFrame


class VideoWindow(QWidget):
    fullScreenSignal = pyqtSignal()

    def __init__(self, stackedWidget):
        super().__init__()
        self.stackedWidget = stackedWidget
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.showMaximized()
        self.player = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.player.setAudioOutput(self.audioOutput)

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
        self.volumeSlider.valueChanged.connect(self.setVolume)
        self.volumeSlider.setEnabled(False)

        # open file button
        self.openFileButton = QPushButton()
        self.openFileButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon))
        self.openFileButton.clicked.connect(self.openFile)
        self.openFileButton.setFixedSize(50, 50)

        # close button
        self.closeButton = QPushButton()
        self.closeButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCloseButton))
        self.closeButton.clicked.connect(self.exitPlayer)
        self.closeButton.setFixedSize(50, 50)

        # full screen button
        self.fullScreenButton = QPushButton()
        self.fullScreenButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarMaxButton))
        self.fullScreenButton.clicked.connect(self.fullScreen)
        self.fullScreenButton.setFixedSize(50, 50)

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

        # add video widget to main layout
        self.videoItem = QGraphicsVideoItem()
        self.scene = QGraphicsScene()
        self.scene.addItem(self.videoItem)
        self.scene.installEventFilter(self)
        self.scene.setBackgroundBrush(Qt.GlobalColor.black)
        self.graphicsView = QGraphicsView(self.scene)
        self.graphicsView.setMouseTracking(True)
        self.graphicsView.setFrameShape(QFrame.Shape.NoFrame)
        self.graphicsView.setCacheMode(QGraphicsView.CacheModeFlag.CacheBackground)
        self.graphicsView.setContentsMargins(0, 0, 0, 0)
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.graphicsView.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        self.player.setVideoOutput(self.videoItem)
        self.player.positionChanged.connect(self.positionChanged)
        self.player.durationChanged.connect(self.durationChanged)
        self.player.mediaStatusChanged.connect(self.mediaStatusChanged)
        self.player.errorOccurred.connect(self.handleError)

        # center video
        self.graphicsView.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # resize event
        self.graphicsView.resizeEvent = self.update_video_widget_size

        # control widget
        self.altLayout = QVBoxLayout()
        self.controlWidget = QWidget()
        self.controlWidget.setFixedHeight(80)
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

    # control layout to hide
    def control_layout_toggle(self, state):
        if state:
            self.controlWidget.setVisible(False)
        else:
            self.controlWidget.setVisible(True)

    # update video widget size
    def update_video_widget_size(self, event):
        self.videoItem.setSize(QSizeF(event.size()))
        self.videoItem.update()
        self.graphicsView.update()
        self.graphicsView.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # play pause video
    def playPause(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.playPauseButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
            self.player.pause()
        else:
            self.playPauseButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
            self.player.play()

    # forward video
    def forward(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.setPosition(self.player.position() + 10000)

    # backward video
    def backward(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.setPosition(self.player.position() - 10000)

    # mute video
    def mute(self):
        if self.player.audioOutput().isMuted():
            self.audioOutput.setMuted(False)
        else:
            self.audioOutput.setMuted(True)

    # volume controller
    def setVolume(self, volume):
        self.audioOutput.setVolume(volume)

    def setPosition(self, position):
        self.player.setPosition(position)

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def set_button_states(self, state):
        self.stopButton.setEnabled(state)
        self.forwardButton.setEnabled(state)
        self.backwardButton.setEnabled(state)
        self.muteButton.setEnabled(state)

    def mediaStatusChanged(self, status):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.playPauseButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
        else:
            self.playPauseButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))

    def handleError(self):
        self.playPauseButton.setEnabled(False)
        self.stopButton.setEnabled(False)
        self.positionSlider.setEnabled(False)
        self.playPauseButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))

    def openFile(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", QDir.homePath())
        if file_name != "":
            self.player.setSource(QUrl.fromLocalFile(file_name))
            self.playPauseButton.setEnabled(True)
            self.set_button_states(True)
            self.positionSlider.setEnabled(True)
            self.player.play()

    def fullScreen(self):
        self.showFullScreen()
        self.controlWidget.setVisible(False)
        self.fullScreenSignal.emit()

    def exitPlayer(self):
        self.player.stop()
        self.close()
        self.stackedWidget.setCurrentIndex(0)

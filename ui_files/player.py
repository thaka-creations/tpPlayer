from PyQt6.QtCore import Qt, QDir, QUrl
from PyQt6.QtGui import QCursor, QMovie, QPainter
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QGraphicsVideoItem
from PyQt6.QtWidgets import QWidget, QApplication, QPushButton, QStyle, QSlider, QHBoxLayout, QVBoxLayout, \
    QGraphicsScene, QFileDialog, QGraphicsView, QFrame


class VideoWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.showMaximized()
        self.player = QMediaPlayer()


        # control buttons
        self.playPauseButton = QPushButton()
        self.playPauseButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.playPauseButton.clicked.connect(self.playPause)
        self.playPauseButton.setFixedSize(50, 50)
        self.playPauseButton.setEnabled(False)

        # stop
        self.stopButton = QPushButton()
        self.stopButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaStop))
        self.stopButton.clicked.connect(self.stop)
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
        self.closeButton.clicked.connect(self.closeEvent)
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

        # add spacer
        self.controlLayout.addStretch(1)
        self.controlLayout.addWidget(self.muteButton)
        self.controlLayout.addWidget(self.volumeSlider)
        self.controlLayout.addWidget(self.fullScreenButton)
        self.controlLayout.addWidget(self.closeButton)

        # add position slider to control layout 2
        self.controlLayout2 = QHBoxLayout()
        self.controlLayout2.addWidget(self.positionSlider)

        # add video widget to main layout
        self.videoItem = QGraphicsVideoItem()
        self.scene = QGraphicsScene()
        self.scene.addItem(self.videoItem)
        self.scene.installEventFilter(self)
        self.scene.setBackgroundBrush(Qt.GlobalColor.black)
        self.graphicsView = QGraphicsView(self.scene)
        self.graphicsView.setMouseTracking(True)
        self.graphicsView.setFrameShape(QFrame.Shape.NoFrame)
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.graphicsView.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        self.player.setVideoOutput(self.videoItem)
        self.player.positionChanged.connect(self.positionChanged)
        self.player.durationChanged.connect(self.durationChanged)
        self.player.mediaStatusChanged.connect(self.mediaStatusChanged)
        self.player.errorOccurred.connect(self.handleError)

        # create main layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.graphicsView)
        self.mainLayout.addLayout(self.controlLayout)
        self.mainLayout.addLayout(self.controlLayout2)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

    # play pause video
    def playPause(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    # stop playing video
    def stop(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.stop()

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
            self.player.audioOutput().setMuted(False)
        else:
            self.player.audioOutput().setMuted(True)

    def setVolume(self, volume):
        self.player.audioOutput().setVolume(volume)

    def setPosition(self, position):
        self.player.setPosition(position)

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def mediaStatusChanged(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.player.stop()
            self.playPauseButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        elif status == QMediaPlayer.MediaStatus.LoadedMedia:
            self.playPauseButton.setEnabled(True)
            self.stopButton.setEnabled(True)
            self.forwardButton.setEnabled(True)
            self.backwardButton.setEnabled(True)
            self.muteButton.setEnabled(True)
            self.volumeSlider.setEnabled(True)
            self.positionSlider.setEnabled(True)
            self.playPauseButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
            self.player.play()

    def handleError(self):
        self.playPauseButton.setEnabled(False)
        self.stopButton.setEnabled(False)
        self.forwardButton.setEnabled(False)
        self.backwardButton.setEnabled(False)
        self.muteButton.setEnabled(False)
        self.volumeSlider.setEnabled(False)
        self.positionSlider.setEnabled(False)
        self.playPauseButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))

    def openFile(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", QDir.homePath())
        if file_name != "":
            self.player.setSource(QUrl.fromLocalFile(file_name))
            self.playPauseButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))

    def fullScreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def closeEvent(self, event):
        self.player.stop()
        self.player.deleteLater()
        event.accept()

    def mouseDoubleClickEvent(self, event):
        cursor_pos = QCursor.pos()
        screen_height = QApplication.primaryScreen().geometry().height()
        if cursor_pos.y() > screen_height - 200:
            self.close()
        return super().mouseDoubleClickEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        return super().keyPressEvent(event)

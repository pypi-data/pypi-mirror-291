# ViCodePy - A video coder for Experimental Psychology
#
# Copyright (C) 2024 Esteban Milleret
# Copyright (C) 2024 Rafael Laboissière
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <https://www.gnu.org/licenses/>.

from PySide6.QtCore import (
    QEvent,
    QSize,
    Qt,
)
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QSplitter,
    QWidget,
)

from .assets import Assets
from .files import Files
from .menu import Menu
from .video import Video
from .timepane import TimePane


class MainWindow(QMainWindow):

    MINIMUM_WIDTH = 640
    MINIMUM_HEIGHT = 320

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ViCodePy")
        self.setMinimumSize(QSize(self.MINIMUM_WIDTH, self.MINIMUM_HEIGHT))

        # FIXME: Move into create_ui
        self.video = Video(self)
        self.time_pane = None

        # Load the QSS file

        with open(Assets().get("style.qss"), "r") as f:
            qss = f.read()

        # FIXME: No need to test existence of qss
        if qss:
            self.setStyleSheet(qss)

        self.installEventFilter(self)

        self.files = Files(self)
        self.files.data_to_load = None

        self.create_ui()

    def create_ui(self):
        """Set up the user interface, signals & slots"""
        splitter = QSplitter(Qt.Orientation.Vertical)
        # FIXME: This is uselless, see below
        widget = QWidget(self)
        self.setCentralWidget(splitter)
        # FIXME: add directly self.video
        splitter.addWidget(widget)

        # Add TimePane
        self.time_pane = TimePane(self)

        # Add the main layout to the main window
        # FIXME: This is uselless, see above
        widget.setLayout(self.video.layout)
        splitter.addWidget(self.time_pane)

        self.menu = Menu(self)

    def on_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def closeEvent(self, event):
        """Display a warning dialog to user when app is closing"""
        if not self.time_pane.has_occurrences():
            return

        action = "ok"
        if self.time_pane.data_needs_save:
            msgBox = QMessageBox(
                QMessageBox.Icon.Warning,
                "Quit the application",
                (
                    "You are about to quit the application. "
                    "The changes made in this session will be lost."
                ),
                QMessageBox.StandardButton.Cancel
                | QMessageBox.StandardButton.Save
                | QMessageBox.StandardButton.Ok,
                self,
            )

            msgBox.button(QMessageBox.StandardButton.Save).setText(
                "Save and Quit"
            )
            msgBox.button(QMessageBox.StandardButton.Ok).setText("Quit")
            msgBox.exec()

            if msgBox.clickedButton() == msgBox.button(
                QMessageBox.StandardButton.Ok
            ):
                action = "ok"
            elif msgBox.clickedButton() == msgBox.button(
                QMessageBox.StandardButton.Save
            ):
                action = "save"
            else:
                action = "ignore"

        if action == "ok":
            # Clean up temp dir
            self.files.temp_dir_cleanup()
            event.accept()
        elif action == "save":
            if self.files.save_project():
                # Clean up temp dir
                self.files.temp_dir_cleanup()
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyRelease:
            if event.key() == Qt.Key.Key_Right:
                if event.isAutoRepeat():
                    if (
                        self.video.media_player.playbackState()
                        != QMediaPlayer.PlaybackState.PlayingState
                    ):
                        self.video.media_player.play()
                else:
                    self.video.media_player.pause()
                return True
        return False

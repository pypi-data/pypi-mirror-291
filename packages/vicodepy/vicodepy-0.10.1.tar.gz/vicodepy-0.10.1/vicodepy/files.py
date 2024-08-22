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

import os
import pandas as pd
import re
import tempfile
import zipfile
import yaml
from math import inf

from PySide6.QtCore import QUrl
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QStyle,
    QVBoxLayout,
)
from PySide6.QtMultimedia import QMediaFormat
from .occurrence import Occurrence
from .coders import Coders
from .config import Config
from .data import Data
from .dialog import DialogCode
from .exceptions import LoadProjectError
from .event import Event, EventCollection
from .format import FORMAT, format_ok
from .timeline import Timeline


class Files:

    # FIXME: move this into data.py
    CSV_HEADERS = ["timeline", "event", "begin", "end", "comment"]

    def __init__(self, window):

        self.window = window
        self.data_to_load = None
        # FIXME: put these in constants.py
        self.csv_delimiter = ","
        self.config_file_name = "config.yml"
        self.metadata_file_name = "metadata.yml"
        self.temp_dir = None
        self.file_format = None
        self.project_file_path = None
        self.coders = None

        # Search for supported video file formats
        self.video_file_extensions = []
        for f in QMediaFormat().supportedFileFormats(QMediaFormat.Decode):
            mime_type = QMediaFormat(f).mimeType()
            name = mime_type.name()
            if re.search("^video/", name):
                self.video_file_extensions.extend(mime_type.suffixes())
        extensions = " ".join(["*." + x for x in self.video_file_extensions])
        self.file_name_filters = [
            f"Video Files ({extensions})",
            "All Files (*.*)",
        ]

        self.project_file_filters = [
            f"Zip files ({' '.join(['*.zip'])})",
            "All Files (*.*)",
        ]

    def open_video(self, widget=None):
        """Open a video file in a MediaPlayer"""
        dialog_txt = "Open Video File"
        file_dialog = QFileDialog(widget) if widget else QFileDialog()
        file_dialog.setWindowTitle(dialog_txt)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilters(self.file_name_filters)
        file_dialog.exec()
        if file_dialog.result() == DialogCode.Accepted:
            # Load only the first of the selected file
            try:
                filename = file_dialog.selectedFiles()[0]
                self.load_video_file(filename)
                self.load_config_file()
            except Exception as e:
                QMessageBox.critical(self.window, "Error", f"{e}")

    def open_project(self, widget=None):
        """Open a project file"""
        dialog_txt = "Open Project File"
        project_dialog = QFileDialog(widget) if widget else QFileDialog()
        project_dialog.setWindowTitle(dialog_txt)
        project_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        project_dialog.setNameFilters(self.project_file_filters)
        project_dialog.exec()
        if project_dialog.result() == DialogCode.Accepted:
            try:
                filename = project_dialog.selectedFiles()[0]
                self.load_project_file(filename)
            except Exception as e:
                QMessageBox.critical(self.window, "Error", f"{e}")

    def load_file(self, filename):
        try:
            if os.path.splitext(filename)[1] in [
                "." + ext for ext in self.video_file_extensions
            ]:
                self.load_video_file(filename)
                self.load_config_file()
            elif os.path.splitext(filename)[1] == ".zip":
                self.load_project_file(filename)
        except Exception as e:
            QMessageBox.critical(self.window, "Error", f"{e}")

    def load_video_file(self, filename):
        """Load video file"""
        if not os.path.exists(filename) or not os.path.isfile(filename):
            raise FileNotFoundError(
                f"FileNotFoundError : {filename} doesn't exist"
            )

        # getOpenFileName returns a tuple, so use only the actual file name
        self.media = QUrl.fromLocalFile(filename)
        self.window.video.media = self.media

        # Enable the buttons
        self.window.video.play_button.setEnabled(True)
        self.window.video.stop_button.setEnabled(True)

        # Put the media in the media player
        self.window.video.media_player.setSource(self.media)

        # Set the title of the track as window title
        self.window.setWindowTitle(os.path.basename(filename))

        # Show first frame
        self.window.video.media_player.play()
        self.window.video.media_player.pause()

        # Clear the time_pane
        if bool(self.media):
            self.window.time_pane.clear()
        self.window.time_pane.load_common()

    def load_project_file(self, filename):
        """Load project file"""
        if not os.path.exists(filename) or not os.path.isfile(filename):
            raise FileNotFoundError(f"FileNotFoundError : {filename} not found")

        # filename is a zip file
        self.project_file_path = filename

        with zipfile.ZipFile(filename, "r") as zip_file:
            # Create temp dir
            temp_dir = tempfile.TemporaryDirectory()

            # Load data from metadata.yml
            with zip_file.open(self.metadata_file_name) as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                self.file_format = data["format"]
                if not format_ok(self.file_format, self.window):
                    raise LoadProjectError("Format problem")
                files = zip_file.namelist()

                # Search for video in temp dir
                video_file = data["video"]
                if video_file not in files:
                    raise LoadProjectError("Failed to load video file")

                # Search for config.yml in temp dir
                if self.config_file_name not in files:
                    raise LoadProjectError("Failed to load config file")

                # Search for csv file in temp dir
                data_file = os.path.splitext(video_file)[0] + ".csv"
                if data_file not in files:
                    raise LoadProjectError("Failed to load data file")

                # Extract all files in temp dir
                zip_file.extractall(temp_dir.name)

                # Load video file from temp dir
                self.load_video_file(os.path.join(temp_dir.name, video_file))

                # Load config file from in temp dir
                self.load_config_file(
                    os.path.join(temp_dir.name, self.config_file_name)
                )

                # Load csv data file from in temp dir
                self.data_to_load = os.path.join(temp_dir.name, data_file)

            self.temp_dir = temp_dir

    def load_config_file(self, filename=None):
        """load presets from config.yml file"""
        # Read the YAML file
        config = Config() if filename is None else Config(filename)

        # Update the config file, eventually
        if self.file_format:
            config.update_format(self.file_format, FORMAT)

        # FIXME: Put this code (or part of it) in timepane.py?
        # Access the values
        if "timelines" in config:

            # Set all absent order fields with Inf
            for k, v in config["timelines"].items():
                if not v:
                    v = dict()
                    config["timelines"][k] = v
                if "order" not in v:
                    v["order"] = -inf
                if "description" not in v:
                    v["description"] = ""

            # Sort according to order first and alphabetically from
            # timeline name, otherwise
            for item in sorted(
                config["timelines"].items(),
                key=lambda x: (x[1]["order"], x[0]),
            ):
                # Get name and properties of the timeline
                name = item[0]
                properties = item[1]

                # Create timeline
                line = Timeline(name, self.window.time_pane)

                # Check description
                description = properties["description"]
                if description == "":
                    description = "(no description)"
                line.label.setToolTip(description)
                line.description = description

                # Add the timeline to the TimePane
                self.window.time_pane.add_timeline(line)

                # Loop over events of the timeline
                # FIXME: do not hardcode here the default color
                DEFAULT_COLOR = QColor(255, 255, 255)
                event_collection = EventCollection()
                if "events" in properties:
                    for k, v in properties["events"].items():
                        event = Event(k)
                        try:
                            event.color = QColor(v["color"])
                        except KeyError:
                            event.color = DEFAULT_COLOR
                        try:
                            event.description = v["description"]
                        except KeyError:
                            event.description = ""
                        event_collection.add_event(event)
                    line.event_collection = event_collection

        if "csv-delimiter" in config:
            self.csv_delimiter = config["csv-delimiter"]

        if "coders" in config:
            self.coders = Coders(config["coders"], self.window)

    def load_data_file(self, filename=None):
        """Load data file"""
        if os.path.isfile(filename):
            data = Data(filename, self.file_format, FORMAT)

            # FIXME: put part of this code in timeline.py?
            for _, row in data.data.iterrows():
                # Search for timeline
                timeline = self.window.time_pane.get_timeline_by_name(
                    row["timeline"]
                )

                # If timeline from csv doesn't exist in TimePane,
                # escape row
                if not timeline:
                    continue

                # Search for event
                event = timeline.event_collection.get_event(row["event"])

                # If event from csv doesn't exist in timeline,
                # then add it
                if not event:
                    continue

                occurrence = Occurrence(
                    self.window.time_pane,
                    timeline,
                    int(row["begin"]),
                    int(row["end"]),
                )

                occurrence.set_event(event)
                occurrence.end_creation()

        else:
            QMessageBox.critical(
                self.window,
                "Error",
                "The file you tried to load does not exist.",
            )

        self.data_to_load = None

    def save_project(self) -> bool:
        """Save project file"""
        temp_dir = tempfile.TemporaryDirectory()

        # Construct the default file name from the QUrl of the video file
        target_directory = self.media.path()
        target_file_name = os.path.splitext(
            os.path.basename(self.media.path())
        )[0]
        data_file_name = target_file_name + ".csv"
        if self.project_file_path:
            target_directory = self.project_file_path
            target_file_name = os.path.splitext(
                os.path.basename(self.project_file_path)
            )[0]

        target_directory = (
            os.path.dirname(target_directory) + "/" + target_file_name + ".zip"
        )

        # 1. Create config file from information of time_pane in
        # tmp directory
        if self.coders:
            if not self.coders.current:
                self.coders.set_current()
        else:
            self.coders = Coders({}, self.window)
            self.coders.set_current()
        self.coders.current.set_date_now()

        config_file_path = os.path.join(temp_dir.name, self.config_file_name)
        self.export_config_file(config_file_path)

        # 2. Create CSV file "data.csv" from information of time_pane in
        # tmp directory
        data_file_path = os.path.join(temp_dir.name, data_file_name)
        self.export_data_file(data_file_path)

        metadata_file_path = os.path.join(
            temp_dir.name, self.metadata_file_name
        )
        with open(metadata_file_path, "w") as f:
            yaml.safe_dump(
                {
                    "video": os.path.basename(self.media.path()),
                    "format": FORMAT,
                },
                f,
            )

        # Open FileDialog
        path, _ = QFileDialog.getSaveFileName(
            self.window,
            "Save project",
            target_directory,
            "Zip Files (*.zip);;All Files (*)",
        )
        if path:
            with zipfile.ZipFile(path, "w") as zip_file:
                zip_file.write(metadata_file_path, self.metadata_file_name)
                zip_file.write(config_file_path, self.config_file_name)
                zip_file.write(data_file_path, data_file_name)
                zip_file.write(
                    self.media.toLocalFile(),
                    os.path.basename(self.media.path()),
                )
            self.window.time_pane.data_needs_save = False
            return True
        return False

    # FIXME: Move this into data.py (?)
    def export_data_file(self, target_path=None) -> bool:
        """Export data in CSV file"""
        if not target_path:
            if not self.is_exportable():
                QMessageBox.warning(
                    self.window, "No Data", "There is no data to save."
                )
                return False

            # Construct the default file name from the QUrl of the video file
            default_target_path = (
                os.path.dirname(self.media.path())
                + "/"
                + os.path.splitext(os.path.basename(self.media.path()))[0]
                + ".csv"
            )

            target_path, _ = QFileDialog.getSaveFileName(
                self.window,
                "Save data (CSV file)",
                default_target_path,
                "CSV Files (*.csv);;All Files (*)",
            )

        if target_path:
            df = pd.DataFrame(columns=self.CSV_HEADERS)
            for timeline in sorted(
                self.window.time_pane.timelines, key=lambda x: x.name
            ):
                for occurrence in timeline.occurrences:
                    comment = occurrence.comment.replace('"', '\\"')
                    row = [
                        timeline.name,
                        occurrence.event.name,
                        occurrence.start_time,
                        occurrence.end_time,
                        comment,
                    ]
                    df.loc[len(df.index)] = row

            df.to_csv(target_path, encoding="utf-8", index=False)
            self.window.time_pane.data_needs_save = False
            return True
        return False

    def is_exportable(self) -> bool:
        """Return true if the media file is exportable"""
        return (
            self.window.video.media_player is not None
            and self.window.time_pane is not None
            and self.window.time_pane.timelines
            and self.window.time_pane.has_occurrences()
        )

    def export_config_file(self, target_path=None):
        config = Config(target_path)

        timelines = self.window.time_pane.timelines
        nb_timelines = len(timelines)

        config["timelines"] = {
            t.name: {
                "order": nb_timelines - i,
                "description": t.description,
                "events": {
                    name: {
                        "color": t.event_collection.get_event(
                            name
                        ).color.name(),
                        "description": t.event_collection.get_event(
                            name
                        ).description,
                    }
                    for name in t.event_collection
                },
            }
            for i, t in enumerate(timelines)
        }

        if self.coders:
            config["coders"] = self.coders.to_list()

        # Write data
        config.save()

    def no_video_loaded(self):
        dialog = OpenProjectDialog(self.window)
        dialog.exec()

    def temp_dir_cleanup(self):
        if self.temp_dir:
            self.temp_dir.cleanup()


class OpenProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Open a project")

        layout = QVBoxLayout(self)

        self.open_video_btn = QPushButton(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon),
            "Open video",
            self,
        )
        self.open_project_btn = QPushButton(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon),
            "Open project",
            self,
        )

        buttons = QDialogButtonBox(self)
        buttons.addButton(
            self.open_video_btn, QDialogButtonBox.ButtonRole.AcceptRole
        )
        buttons.addButton(
            self.open_project_btn, QDialogButtonBox.ButtonRole.AcceptRole
        )
        buttons.addButton(QDialogButtonBox.StandardButton.Cancel)

        buttons.clicked.connect(self.perform_action)
        buttons.rejected.connect(self.reject)

        layout.addWidget(
            QLabel("Choose a video or a project file to start coding")
        )
        layout.addWidget(buttons)
        self.setLayout(layout)

    def perform_action(self, button):
        if button == self.open_video_btn:
            self.parent().files.open_video(self)
        elif button == self.open_project_btn:
            self.parent().files.open_project(self)
        self.accept()

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

from abc import abstractmethod

from PySide6.QtCore import (
    Qt,
    QRectF,
)
from PySide6.QtGui import (
    QColor,
    QPen,
)
from PySide6.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsItem,
    QMenu,
    QMessageBox,
)

from .utils import color_fg_from_bg
from .comment import OccurrenceComment
from .event import ChooseEvent


class Occurrence(QGraphicsRectItem):
    DEFAULT_PEN_COLOR = QColor(0, 0, 0)
    DEFAULT_BG_COLOR = QColor(128, 128, 128)
    DEFAULT_FONT_COLOR = QColor(0, 0, 0)
    PEN_WIDTH_ON_CURSOR = 3
    PEN_WIDTH_OFF_CURSOR = 1

    # FIXME: Change nomenclature "start" ⇒ "begin"

    def __init__(
        self,
        # FIXME: get from timeline
        time_pane,
        timeline,
        # FIXME: {start,end}_time should not be None by default. The only place where it is used in this way is in timepane.py, when creating a new occurrence. It should be the reponsability of the calling to code to adust the correct {start,end} time when instanciating the Occcurrence object.
        start_time: int = None,
        end_time: int = None,
        # FIXME: are those really needed?
        lower_bound: int = None,
        upper_bound: int = None,
    ):
        """Initializes the Occurrence widget"""
        super().__init__(timeline)
        # FIXME: Use underscore instead of cammelCase style
        self.brushColor = self.DEFAULT_BG_COLOR
        # FIXME: Use underscore instead of cammelCase style
        self.penColor = self.DEFAULT_PEN_COLOR
        # FIXME: Use underscore instead of cammelCase style
        self.penWidth = self.PEN_WIDTH_OFF_CURSOR
        # FIXME: Use underscore instead of cammelCase style
        self.fontColor = self.DEFAULT_FONT_COLOR
        self.event = None
        self.name = None
        self.time_pane = time_pane
        self.mfps = self.time_pane.video.mfps
        # FIXME: See above
        self.start_time = (
            start_time if start_time else time_pane.value - int(self.mfps / 2)
        )
        self.end_time = (
            end_time if end_time else time_pane.value + int(self.mfps / 2)
        )
        self.timeline = timeline
        # FIXME: {start,end}_x_position do not to be instance attributes
        # FIXME: use variable factor = self.time_pane.scene.width() / self.time_pane.duration, in order to avoid code repetition
        self.start_x_position = int(
            self.start_time
            * self.time_pane.scene.width()
            / self.time_pane.duration
        )
        self.end_x_position = int(
            self.end_time
            * self.time_pane.scene.width()
            / self.time_pane.duration
        )
        # FIXME: put code of method set_default_rect here
        self.set_default_rect()
        self.selected = False
        self.begin_handle: OccurrenceHandle = None
        self.end_handle: OccurrenceHandle = None

        self.setX(self.start_x_position)
        self.setY(self.timeline.label.FIXED_HEIGHT)
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.comment: str = ""

    # FIXME: move into Timeline
    def can_be_initiated(occurrences, value):
        """Check if the occurrence can be initiated"""
        lower_bound = upper_bound = None
        valid = True
        occurrence_under_cursor = None

        # Loop through the occurrences of the selected timeline
        for a in occurrences:
            if a.start_time <= value <= a.end_time:
                valid = False
                occurrence_under_cursor = a
                break
            if not lower_bound:
                if a.end_time < value:
                    lower_bound = a.end_time + int(a.mfps / 2)
            else:
                if a.end_time < value:
                    if lower_bound < a.end_time:
                        lower_bound = a.end_time + int(a.mfps / 2)
            if not upper_bound:
                if a.start_time > value:
                    upper_bound = a.start_time - int(a.mfps / 2)
            else:
                if a.start_time > value:
                    if upper_bound > a.start_time:
                        upper_bound = a.start_time - int(a.mfps / 2)
        return valid, lower_bound, upper_bound, occurrence_under_cursor

    # FIXME: Drop this method (see above)
    def set_default_rect(self):
        self.setRect(
            QRectF(
                0,
                0,
                self.end_x_position - self.start_x_position,
                self.timeline.FIXED_HEIGHT - self.timeline.label.FIXED_HEIGHT,
            )
        )

    def mousePressEvent(self, event):
        if not self.time_pane.occurrence_in_creation:
            self.time_pane.select_timeline(self.timeline)

    def mouseReleaseEvent(self, event):
        return

    def mouseDoubleClickEvent(self, event):
        if not self.time_pane.occurrence_in_creation:
            self.setSelected(True)
            self.get_bounds()
            self.time_pane.select_timeline(self.timeline)

    def focusOutEvent(self, event):
        self.setSelected(False)
        super().focusOutEvent(event)

    def contextMenuEvent(self, event):
        if not self.isSelected():
            super().contextMenuEvent(event)
            return
        can_merge_previous = False
        for occurrence in self.timeline.occurrences:
            if (
                occurrence.end_time == self.start_time
                and self.name == occurrence.name
            ):
                can_merge_previous = True
                break
        can_merge_next = False
        for occurrence in self.timeline.occurrences:
            if (
                self.end_time == occurrence.start_time
                and self.name == occurrence.name
            ):
                can_merge_next = True
                break
        menu = QMenu()
        menu.addAction("Delete occurrence").triggered.connect(self.on_remove)
        menu.addAction("Change occurrence label").triggered.connect(
            self.change_event
        )
        if can_merge_previous:
            menu.addAction("Merge with previous occurrence").triggered.connect(
                self.merge_previous
            )
        if can_merge_next:
            menu.addAction("Merge with next occurrence").triggered.connect(
                self.merge_next
            )
        menu.addAction("Comment occurrence").triggered.connect(
            self.edit_comment
        )
        menu.exec(event.screenPos())

    def on_remove(self):
        answer = QMessageBox.question(
            self.time_pane,
            "Confirmation",
            "Do you want to remove the occurrence?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if answer == QMessageBox.StandardButton.Yes:
            self.remove()

    def edit_comment(self):
        comment_dialog = OccurrenceComment(self.comment, self.time_pane)
        comment_dialog.exec()
        if comment_dialog.result() == QMessageBox.DialogCode.Accepted:
            self.comment = comment_dialog.get_text()
        self.setToolTip(self.comment)

    def merge_previous(self):
        for occurrence in self.timeline.occurrences:
            if (
                self.start_time == occurrence.end_time
                and self.name == occurrence.name
            ):
                break
        self.start_time = occurrence.start_time
        occurrence.remove()
        self.update_rect()
        self.update()

    def merge_next(self):
        for occurrence in self.timeline.occurrences:
            if (
                self.end_time == occurrence.start_time
                and self.name == occurrence.name
            ):
                break
        self.end_time = occurrence.end_time
        occurrence.remove()
        self.update_rect()
        self.update()

    def change_event(self):
        events_dialog = ChooseEvent(
            self.timeline.event_collection, self.timeline.time_pane
        )
        events_dialog.exec()
        if events_dialog.result() == QMessageBox.DialogCode.Accepted:
            event = events_dialog.get_chosen()
            self.set_event(event)
            self.update()

    # FIXME: Move part of this into Timeline (?)
    def remove(self):
        self.time_pane.scene.removeItem(self)
        if self in self.timeline.occurrences:
            self.timeline.remove_occurrence(self)
        del self

    # FIXME: Use None instead of Ellipsis
    def paint(self, painter, option, widget=...):
        # Draw the occurrence rectangle
        self.draw_rect(painter)

        # Draw the name of the occurrence in the occurrence rectangle
        self.draw_name(painter)

        if self.isSelected():
            self.show_handles()
        else:
            self.hide_handles()

    def draw_rect(self, painter):
        """Draw the occurrence rectangle"""
        pen: QPen = QPen(self.penColor)
        pen.setWidth(self.penWidth)

        if self.isSelected():
            # Set border dotline if occurrence is selected
            pen.setStyle(Qt.PenStyle.DotLine)
        painter.setPen(pen)
        painter.setBrush(self.brushColor)

        # Draw the rectangle
        painter.drawRect(self.rect())

    def draw_name(self, painter):
        """Draws the name of the occurrence"""
        if self.name:
            col = color_fg_from_bg(self.brushColor)
            painter.setPen(col)
            painter.setBrush(col)
            painter.drawText(
                self.rect(), Qt.AlignmentFlag.AlignCenter, self.name
            )

    def set_event(self, event=None):
        """Updates the event"""
        if event is None:
            self.event = None
            self.brushColor = self.DEFAULT_BG_COLOR
        else:
            self.event = event
            self.brushColor = event.color
            self.name = event.name
            self.setToolTip(
                self.comment if self.comment != "" else "(no comment)"
            )
            if self.begin_handle:
                self.begin_handle.setBrush(event.color)
                self.end_handle.setBrush(event.color)

    def update_style(self):
        if self.event:
            self.brushColor = self.event.color
            self.name = self.event.name

    # FIXME: Drop useless argument new_rect
    def update_rect(self, new_rect: QRectF = None):
        new_rect = new_rect or self.time_pane.scene.sceneRect()
        # Calculate position to determine width
        # FIXME: Use local variables {start,end}_x_position
        # FIXME: Use variable factor = new_rect.width() / self.time_pane.duration
        self.start_x_position = (
            self.start_time * new_rect.width() / self.time_pane.duration
        )
        self.end_x_position = (
            self.end_time * new_rect.width() / self.time_pane.duration
        )
        self.setX(self.start_x_position)

        # Update the rectangle
        rect = self.rect()
        rect.setWidth(self.end_x_position - self.start_x_position)
        self.setRect(rect)

        if self.begin_handle:
            self.begin_handle.setX(self.rect().x())
            self.end_handle.setX(self.rect().width())

    def update_start_time(self, start_time: int):
        self.start_time = start_time
        self.update_rect()
        self.update()

    def update_end_time(self, end_time: int):
        """Updates the end time"""
        self.end_time = end_time
        self.update_rect()
        self.update()

    def update_selectable_flags(self):
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.update()

    def create_handles(self):
        self.begin_handle = OccurrenceStartHandle(self)
        self.end_handle = OccurrenceEndHandle(self)

    def end_creation(self):
        """Ends the creation of the occurrence"""
        self.update_selectable_flags()
        self.create_handles()

        # if start_time is greater than end_time then swap times
        if self.start_time > self.end_time:
            self.start_time, self.end_time = self.end_time, self.start_time
            self.update_rect()

        # Add this occurrence to the occurrence list of the timeline
        self.timeline.add_occurrence(self)

        self.update()

    def show_handles(self):
        if self.begin_handle:
            self.begin_handle.setVisible(True)
        if self.end_handle:
            self.end_handle.setVisible(True)

    def hide_handles(self):
        if self.begin_handle:
            self.begin_handle.setVisible(False)
        if self.end_handle:
            self.end_handle.setVisible(False)

    def get_bounds(self):
        _, lower_bound, upper_bound, occurrence = Occurrence.can_be_initiated(
            list(filter(lambda x: x != self, self.timeline.occurrences)),
            self.start_time,
        )
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def get_time_from_bounding_interval(self, time) -> int:
        if self.lower_bound and time < self.lower_bound:
            time = self.lower_bound
        elif self.upper_bound and time > self.upper_bound:
            time = self.upper_bound
            self.time_pane.video.media_player.pause()
        return time


class OccurrenceHandle(QGraphicsRectItem):
    PEN_WIDTH_ON = 3
    PEN_WIDTH_OFF = 1
    HANDLE_WIDTH = 9

    def __init__(self, occurrence: Occurrence, value: int, x: float):
        super().__init__(occurrence)
        self.occurrence = occurrence
        self.value = value

        self.pen: QPen = QPen(self.occurrence.penColor)
        self.pen.setWidth(self.PEN_WIDTH_OFF)
        self.setPen(self.pen)
        self.setBrush(self.occurrence.brushColor)
        self.setVisible(False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.setAcceptDrops(True)

        self.height = occurrence.rect().height() / 2
        self.setRect(
            QRectF(-self.HANDLE_WIDTH / 2, 0, self.HANDLE_WIDTH, self.height)
        )

        self.setX(x)
        self.setY(self.height / 2)

    @abstractmethod
    def change_time(self, new_time):
        self.value = new_time

    def focusInEvent(self, event):
        self.occurrence.setSelected(True)
        self.occurrence.time_pane.video.set_position(self.value)
        self.pen.setWidth(self.PEN_WIDTH_ON)
        self.setPen(self.pen)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.occurrence.setSelected(False)
        self.pen.setWidth(self.PEN_WIDTH_OFF)
        self.setPen(self.pen)
        super().focusOutEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.setY(self.height / 2)

            # With the mouse, the coordinate X is changed, but we need to
            # change the time.
            time = int(
                event.scenePos().x()
                * self.occurrence.time_pane.duration
                / self.occurrence.time_pane.scene.width()
            )

            time = self.occurrence.get_time_from_bounding_interval(time)

            self.occurrence.time_pane.video.set_position(time)


class OccurrenceStartHandle(OccurrenceHandle):

    def __init__(self, occurrence: Occurrence):
        super().__init__(occurrence, occurrence.start_time, 0)

    def change_time(self, time):
        t = time - int(self.occurrence.mfps / 2)
        super().change_time(t)
        self.occurrence.update_start_time(t)


class OccurrenceEndHandle(OccurrenceHandle):
    def __init__(self, occurrence: Occurrence):
        super().__init__(
            occurrence, occurrence.end_time, occurrence.rect().width()
        )

    def change_time(self, time):
        t = time + int(self.occurrence.mfps / 2)
        super().change_time(t)
        self.occurrence.update_end_time(t)

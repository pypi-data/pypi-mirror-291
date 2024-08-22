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
    Qt,
    QPointF,
)
from PySide6.QtGui import (
    QColor,
    QFontMetrics,
)
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGraphicsRectItem,
    QGraphicsItem,
    QLineEdit,
    QMenu,
    QMessageBox,
)

from .event import ChangeEvent, ChooseEvent
from .textedit import TextEdit


class Timeline(QGraphicsRectItem):
    FIXED_HEIGHT: float = 60.0

    # FIXME: It seems that time_pane is always passed as argument
    def __init__(self, name: str, time_pane=None):
        super().__init__()
        self.name = name
        self.time_pane = time_pane
        self.occurrences = []
        self.events = None
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.setAcceptHoverEvents(True)
        # FIXME: Change nomenclature "label" ⇒ "title"
        self.label = TimelineLabel(self.name, self)
        self._select = False
        self.description = None

    @property
    def select(self):
        return self._select

    @select.setter
    def select(self, select):
        if select != self._select:
            self._select = select

    # FIXME: move into TimePane
    def add_to_scene(self):
        """Add the timeline to the scene"""
        # Set Y of the timeline based on the timescale height and the timeline
        # lines heights present on the scene
        self.setPos(
            0,
            # FIXME: Can't we use self.time_pane.time_pane_scale.FIXED_HEIGHT
            self.time_pane.time_pane_scale.rect().height()
            + (len(self.time_pane.timelines) - 1) * self.FIXED_HEIGHT,
        )

        # Set the right rect based on the scene width and the height constant
        self.setRect(
            0,
            0,
            self.time_pane.scene.width(),
            self.FIXED_HEIGHT,
        )

        # Add line to the scene
        self.time_pane.scene.addItem(self)

    def add_event(self, event):
        """Add an event to the timeline"""
        self.events.add_event(event)
        # FIXME: Drop the following line; it seems useless
        self.events.sort(key=lambda x: x.name.lower())

    # FIXME: Check whether this is still necessary
    def remove_event(self, event):
        """Remove a event from the timeline"""
        self.events.remove(event)

    # FIXEME: Remove this method, it is never used
    def get_event_by_name(self, name):
        return next((x for x in self.events if x.name == name), None)

    def add_occurrence(self, occurrence):
        """Add an occurrence to the timeline"""
        self.occurrences.append(occurrence)
        self.occurrences.sort(key=lambda x: x.start_time)
        # FIXME: Do not set flag when adding occurrences. Only set it when a *new* one is created.
        self.time_pane.data_needs_save = True

    def remove_occurrence(self, occurrence):
        """Remove an occurrence from the timeline"""
        self.occurrences.remove(occurrence)
        # FIXME: Also delete the ocurrence object

    def update_rect_width(self, new_width: float):
        """Update the width of the timeline"""
        rect = self.rect()
        rect.setWidth(new_width)
        # FIXME: Move the following into TimelineLabel
        rect_label = self.label.rect()
        rect_label.setWidth(new_width)
        self.label.setRect(rect_label)
        self.setRect(rect)

    def on_remove(self):
        if self.occurrences:
            answer = QMessageBox.question(
                self.time_pane,
                "Confirmation",
                "There are occurrences present. "
                "Do you want to remove this timeline?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if answer == QMessageBox.StandardButton.Yes:
                while self.occurrences:
                    # FIXME: Use remove_occurence method
                    self.occurrences[0].remove()
        # The following does not yet work, since there is no provision for
        # adjusting the positions of the timelines inside the time pane.
        # self.time_pane.scene.removeItem(self)
        # if self in self.time_pane.timelines:
        #     self.time_pane.timelines.remove(self)
        # del self

    # FIXME: Move into class TimelineLabel
    def edit_properties(self):
        dialog = QDialog(self.time_pane)
        dialog.setWindowTitle("Timeline properties")

        layout = QFormLayout(self.time_pane)
        self.name_edit = QLineEdit()
        self.name_edit.setText(self.label.text)
        self.name_edit.returnPressed.connect(dialog.accept)
        layout.addRow("Name: ", self.name_edit)
        layout.addRow("Description:", None)
        self.description_edit = TextEdit(self, self.description)
        layout.addRow(self.description_edit)
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
            self.time_pane,
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.setLayout(layout)

        dialog.exec()
        if dialog.result() == dialog.DialogCode.Accepted:
            self.label.text = self.name_edit.text()
            self.description = self.description_edit.toPlainText()
            self.label.setToolTip(self.description)

    def update_occurrences(self):
        for occurrence in self.occurrences:
            occurrence.update_style()

    def edit_events(self):
        while True:
            events_dialog = ChooseEvent(self.event_collection, self.time_pane)
            events_dialog.exec()
            if events_dialog.result() == QMessageBox.DialogCode.Accepted:
                e = events_dialog.get_chosen()
                ChangeEvent(e, self.time_pane).exec()
                self.update_occurrences()
            if events_dialog.result() == QMessageBox.DialogCode.Rejected:
                break

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            menu = QMenu()
            menu.addAction("Add new timeline").triggered.connect(
                self.time_pane.handle_timeline
            )
            menu.addAction(
                "Delete timeline (not yet fully implemented)"
            ).triggered.connect(self.on_remove)
            menu.addAction("Edit timeline properties").triggered.connect(
                self.edit_properties
            )
            menu.addAction("Edit events").triggered.connect(self.edit_events)
            menu.exec(event.screenPos())
        else:
            super().mousePressEvent(event)
        return


class TimelineLabel(QGraphicsRectItem):
    FIXED_HEIGHT = 20

    def __init__(self, text: str, parent: Timeline = None):
        super().__init__(parent)
        self.text = text
        rect = self.parentItem().rect()
        rect.setHeight(self.FIXED_HEIGHT)
        self.setRect(rect)
        self.parent = parent

    def paint(self, painter, option, widget=...):
        # Draw the rectangle
        self.draw_rect(painter)

        # Draw the text
        self.draw_text(painter)

    # FIXME: In methods draw_rect and draw_text, do not hardcode the
    # colors. Use class varaibles, instead.

    def draw_rect(self, painter):
        """Draw the timeline label rectangle"""
        # Set Pen and Brush for rectangle
        if self.parent.select:
            color = QColor(40, 40, 40)
        else:
            color = QColor(200, 200, 200)
        painter.setPen(color)
        painter.setBrush(color)
        painter.drawRect(self.rect())

    def draw_text(self, painter):
        """Draw the timeline label text"""
        if self.parent.select:
            color = QColor(200, 200, 200)
        else:
            color = QColor(150, 150, 150)
        painter.setPen(color)
        painter.setBrush(color)

        font = painter.font()
        fm = QFontMetrics(font)

        text_width = fm.boundingRect(self.text).width()
        text_height = fm.boundingRect(self.text).height()
        # Get timeline polygon based on the viewport
        timeline_in_viewport_pos = self.parentItem().time_pane.view.mapToScene(
            self.rect().toRect()
        )

        bounding_rect = timeline_in_viewport_pos.boundingRect()

        # Get the viewport rect
        viewport_rect = self.parentItem().time_pane.view.viewport().rect()

        # Compute the x position for the text
        x_alignCenter = bounding_rect.x() + viewport_rect.width() / 2

        # FIXME: Do not hardcode the value "3"
        text_position = QPointF(x_alignCenter - text_width / 2, text_height - 3)

        painter.drawText(text_position, self.text)

    # FIXME: Use @property? Anyway, check whether this is really needed
    def set_text(self, text):
        self.text = text

import time

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import (
    QGraphicsItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
    QStatusBar,
)

from infinote.buffer_handling import BufferHandler
from infinote.config import Config
from infinote.key_handler import KeyHandler
from infinote.text_object import BoxInfo, DraggableText, EditorBox


def _exit_visual_mode(nvim):
    mode = nvim.api.get_mode()["mode"]
    if mode == "v" or mode == "V" or mode == "\x16":
        nvim.input("<Esc>")


class GraphicView(QGraphicsView):
    def __init__(self, nvim, main_subdir, parent=None):
        super().__init__(parent)
        self.nvim = nvim
        self.setRenderHint(QPainter.Antialiasing)
        self.setBackgroundBrush(QColor(Config.background_color))
        self.setScene(QGraphicsScene())
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.global_scale = 1.0
        self.key_handler = KeyHandler(nvim, self)
        self.buf_handler = BufferHandler(nvim, self)
        self.current_folder = main_subdir
        self.workspace_dir = main_subdir.parent
        self.timer = None
        self._timer_last_update = None

        # dummy object so that the text boxes can be unfocused
        dummy = QGraphicsRectItem()
        dummy.setFlag(QGraphicsItem.ItemIsFocusable)
        self.scene().addItem(dummy)
        self.dummy = dummy

        # create a status bar
        screen_size = self.screen().size()
        self.status_bar = QStatusBar()
        # place it at the top and display
        # 20 is added to hide the weird handle on the right
        self.status_bar.setGeometry(0, 0, screen_size.width() + 20, 20)
        color = Config.background_color
        self.status_bar.setStyleSheet("QStatusBar{background-color: " + color + ";}")
        self._message = []
        self.scene().addWidget(self.status_bar)

        self.editor_box = EditorBox(nvim, self.nvim.current.buffer, self)
        self.scene().addItem(self.editor_box)
        self.show_editor = True

    def _render_status_bar(self):
        mode_dict = self.nvim.api.get_mode()
        if not mode_dict["blocking"]:
            num_unbound_bufs = self.buf_handler.get_num_unbound_buffers()
            if num_unbound_bufs > 0:
                self.msg(f"{num_unbound_bufs} unbound buffer exists - click somewhere to place it")

            if mode_dict["mode"] == "c":
                # the command mode was entered not by us, but externally
                # (we never actually enter it from infinote)
                # here we only try to match what is being input into the command line
                self.key_handler.external_command_mode = True

        command_line = self.key_handler.get_command_line()
        if command_line:
            self._message = [command_line] + self._message

        msg_string = " | ".join(self._message)
        self.status_bar.showMessage(msg_string)

    # event handling methods
    # note: there's one more possible event: mouseMoveEvent, but it's handled by texts

    def resizeEvent(self, event):
        self.scene().setSceneRect(0, 0, event.size().width(), event.size().height())
        super().resizeEvent(event)

    def mousePressEvent(self, event):
        # ignore non-left clicks
        if event.button() != Qt.LeftButton:
            return
        self._message = []
        item = self.scene().itemAt(event.screenPos(), self.transform())

        if isinstance(item, DraggableText):
            # clicked on text, so make it current
            self.buf_handler.jump_to_buffer(item.buffer.number)
            self.buf_handler.update_all_texts()

            # pin the click position, in case of dragging
            click_pos = event.screenPos() / self.global_scale
            item._pin_pos = (click_pos - item.plane_pos_vect) / item.get_plane_scale()
            
            # we need to first process the click by the widget to set cursor in it
            # we also need to pass the event, in case it's a drag event
            super().mousePressEvent(event)
            item.insides_renderer.sync_qt_cursor_into_vim(self.nvim)
            # note: maybe that makes dragging less efficient, but we need to do it to set the cursor
            self.buf_handler.update_all_texts()

        elif isinstance(item, EditorBox):
            _exit_visual_mode(self.nvim)
            # we need to first process the click by the widget to set cursor in it
            super().mousePressEvent(event)
            item.insides_renderer.sync_qt_cursor_into_vim(self.nvim)
            self.buf_handler.update_all_texts()
        else:
            # clicked bg, so create a new text
            item = self.buf_handler.create_text(
                self.current_folder,
                BoxInfo(plane_pos=(event.screenPos() / self.global_scale).toTuple()),
            )
            self.buf_handler.update_all_texts()
            # super().mousePressEvent(event)

        if self.show_editor:
            self.editor_box.setFocus()
        else:
            item.setFocus()
        self._render_status_bar()

    def keyPressEvent(self, event):
        self._message = []

        self.editor_box.insides_renderer.if_qt_selection_sync_into_vim(self.nvim)

        self.key_handler.handle_key_event(event)
        self.buf_handler.update_all_texts()
        self._render_status_bar()

    def wheelEvent(self, event):
        direction = -1 if Config.scroll_invert else 1
        zoom_factor = Config.scroll_speed ** (event.angleDelta().y() * direction)

        item = self.scene().itemAt(event.position(), self.transform())
        if isinstance(item, EditorBox):
            # handle text scroll normally
            super().wheelEvent(event)
        # elif isinstance(item, DraggableText) and Config.scroll_can_resize_text:
        #     # zoom it
        #     item.manual_scale *= zoom_factor
        #     item.reposition()
        else:
            # zoom the whole view
            self.global_scale *= zoom_factor

            # reposition all texts
            for text in self.buf_handler.get_root_texts():
                text.reposition()

    def msg(self, msg):
        self._message.append(msg)

    def jump_to_neighbor(self, direction: str):
        current_text = self.buf_handler.get_current_text()
        new = self._get_closest_text(current_text, direction)
        if new is None:
            return

        buf_num = new.buffer.number
        self.buf_handler.jump_to_buffer(buf_num)

        if Config.track_jumps_on_neighbor_moves:
            self.track_jump(current_text, new)

        self.zoom_on_text(new)

    def track_jump(self, old, new):
        # update global scale to track the movement
        old_pos = old.plane_pos_vect
        old_dist = (old_pos.x() ** 2 + old_pos.y() ** 2) ** 0.5
        new_pos = new.plane_pos_vect
        new_dist = (new_pos.x() ** 2 + new_pos.y() ** 2) ** 0.5

        self.global_scale *= old_dist / new_dist

    def zoom_on_text(self, text):
        # keep the text in view
        smallest_scale = self.get_scale_centered_on_text(text)
        biggest_scale = self.get_scale_maximized_on_text(text)
        self.global_scale = min(biggest_scale, self.global_scale)
        self.global_scale = max(smallest_scale, self.global_scale)

    def get_scale_centered_on_text(self, text):
        window_width = self.screen().size().width()
        window_height = self.screen().size().height()
        if self.show_editor:
            window_width *= 1 - Config.editor_width_ratio

        x, y = text.plane_pos
        center_scale_x = window_width / (x * 2 + text.get_plane_width())
        center_scale_y = window_height / (y * 2 + text.get_plane_height())

        return min(center_scale_x, center_scale_y)

    def get_scale_maximized_on_text(self, text):
        window_width = self.screen().size().width()
        window_height = self.screen().size().height()
        if self.show_editor:
            window_width *= 1 - Config.editor_width_ratio

        x, y = text.plane_pos
        width_scale = window_width / (x + text.get_plane_width())
        width_scale *= 1 - Config.min_gap_win_edge * 9 / 16
        height_scale = window_height / (y + text.get_plane_height())
        height_scale *= 1 - Config.min_gap_win_edge

        return min(width_scale, height_scale)

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            return

        if self.timer is not None:
            self.timer.stop()
            self.timer = None
            self._timer_last_update = None

    def zoom(self, sign):
        if self._timer_last_update is None:
            # timer just starting
            self._timer_last_update = time.time()
            return
        new_time = time.time()
        time_diff = new_time - self._timer_last_update
        self._timer_last_update = new_time

        self.global_scale *= Config.key_zoom_speed ** (time_diff * sign)

        # reposition all texts
        for text in self.buf_handler.get_root_texts():
            text.reposition()

    def resize(self, sign):
        if self._timer_last_update is None:
            # timer just starting
            self._timer_last_update = time.time()
            return
        new_time = time.time()
        time_diff = new_time - self._timer_last_update
        self._timer_last_update = new_time

        # resize current text box
        text = self.buf_handler.get_current_text()
        delta = Config.key_zoom_speed ** (time_diff * sign)
        if text.parent_filename is None:
            text.manual_scale *= delta
        else:
            text.scale_rel_to_parent *= delta
        text.reposition()

    def _get_closest_text(self, current_text, direction):
        current_center = current_text.get_center()

        # get all texts in that direction
        candidate_text_distances = dict()
        for text in self.buf_handler.get_texts():
            if text == current_text:
                continue
            diff = text.get_center() - current_center
            x, y = diff.x(), diff.y()

            if (
                (direction == "down" and y >= abs(x))
                or (direction == "right" and x >= abs(y))
                or (direction == "up" and y <= -abs(x))
                or (direction == "left" and x <= -abs(y))
            ):
                candidate_text_distances[text] = (x**2 + y**2) ** 0.5

        if len(candidate_text_distances) == 0:
            return None

        # get the closest one
        return min(candidate_text_distances.keys(), key=candidate_text_distances.get)

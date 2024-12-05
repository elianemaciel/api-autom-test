from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QPainterPath
from PySide6.QtWidgets import QComboBox


class CustomComboBox(QComboBox):
    def __init__(self, do_after_set_index=lambda index: None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.do_after_set_index = do_after_set_index
        self.currentIndexChanged.connect(self.handle_index_change)
        self.curr_index = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Background color
        background_color = QColor(0, 240, 0)
        painter.setBrush(QBrush(background_color))
        painter.setPen(QPen(background_color))

        # Round corners
        radius = 10.0
        path = QPainterPath()
        path.addRoundedRect(self.rect(), radius, radius)
        painter.drawPath(path)

        super().paintEvent(event)

    def handle_index_change(self, index):
        if index != self.curr_index:
            # print("handle_index_change: " + str(index))
            self.do_after_set_index(index)
            self.curr_index = index

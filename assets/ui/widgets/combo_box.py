from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QPainterPath
from PySide6.QtWidgets import QComboBox


class CustomComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
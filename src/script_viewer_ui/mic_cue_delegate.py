from PyQt5.QtCore import QModelIndex, QRect, QSize, Qt
from PyQt5.QtGui import QColor, QFont, QFontMetrics, QPainter
from PyQt5.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem

from block import Block
from script_viewer_ui import theme
from script_viewer_ui.block_table_model import BLOCK_ROLE, IS_CURRENT_ROLE

UNMUTE_PREFIX = "▲ "
MUTE_PREFIX = "▼ "
PADDING = 4


class MicCueDelegate(QStyledItemDelegate):
    """Paints the mic column: one line per actor, unmutes in green above mutes in red.

    A plain item can only have a single text color, so the mixed list of mutes
    and unmutes of a block is painted by hand.
    """

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        painter.save()
        painter.fillRect(option.rect, index.data(Qt.BackgroundRole))

        is_current = index.data(IS_CURRENT_ROLE)
        font = self._font()
        painter.setFont(font)
        line_height = QFontMetrics(font).lineSpacing()

        line_rect = QRect(option.rect.adjusted(PADDING, PADDING, -PADDING, 0))
        line_rect.setHeight(line_height)
        for text, color in self._lines(index.data(BLOCK_ROLE), is_current):
            painter.setPen(color)
            painter.drawText(line_rect, Qt.AlignLeft | Qt.AlignVCenter, text)
            line_rect.translate(0, line_height)

        painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        metrics = QFontMetrics(self._font())
        lines = self._lines(index.data(BLOCK_ROLE), is_current=True)
        width = max((metrics.horizontalAdvance(text) for text, _ in lines), default=0)
        return QSize(width + 2 * PADDING, len(lines) * metrics.lineSpacing() + 2 * PADDING)

    @staticmethod
    def _lines(block: Block, is_current: bool) -> list[tuple[str, QColor]]:
        unmute_color = theme.UNMUTE if is_current else theme.DIMMED_UNMUTE
        mute_color = theme.MUTE if is_current else theme.DIMMED_MUTE
        return ([(UNMUTE_PREFIX + name, unmute_color) for name in block.unmute]
                + [(MUTE_PREFIX + name, mute_color) for name in block.mute])

    @staticmethod
    def _font() -> QFont:
        font = QFont()
        font.setPointSize(theme.FONT_POINT_SIZE)
        font.setBold(True)
        return font

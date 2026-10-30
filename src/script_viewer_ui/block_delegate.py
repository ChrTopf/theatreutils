import html
import math

from PyQt5.QtCore import QModelIndex, QRect, QRectF, QSize, Qt
from PyQt5.QtGui import QColor, QPainter, QPen, QTextDocument
from PyQt5.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem

from model.block import Block
from script_viewer_ui import theme
from script_viewer_ui.block_list_model import BLOCK_ROLE, IS_CURRENT_ROLE
from script_viewer_ui.cue_lanes import LANES, CueLane, CueLaneSegments
from script_viewer_ui.cue_style import CueStyle
from script_viewer_ui.row_layout import RowLayout


class BlockDelegate(QStyledItemDelegate):
    """Paints one block as a card of a document: the character above the text. Its cues are shown in the cue lanes."""

    def __init__(self, cue_lanes: CueLaneSegments, parent=None):
        super().__init__(parent)
        self._cue_lanes = cue_lanes
        self._visible_lanes = LANES
        self._viewport_width = 0
        self._card_heights: dict[tuple[int, int], int] = {}

    def set_visible_lanes(self, lanes: tuple[CueLane, ...]) -> None:
        """Tells the delegate which cue lanes share the row with the cards, which changes their width and height."""
        self._visible_lanes = lanes
        self._card_heights.clear()

    def set_viewport_width(self, width: int) -> bool:
        """Tells the delegate how wide the cards may be. Returns True if that changed the layout."""
        if width == self._viewport_width:
            return False
        self._viewport_width = width
        self._card_heights.clear()
        return True

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        block = index.data(BLOCK_ROLE)
        is_current = index.data(IS_CURRENT_ROLE)
        layout = self._row_layout(option.rect)
        card = layout.card_rect(option.rect.y(), option.rect.height() - theme.BLOCK_SPACING)

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)
        self._paint_card(painter, card, is_current)

        content = card.adjusted(theme.BLOCK_PADDING, theme.BLOCK_PADDING, -theme.BLOCK_PADDING, -theme.BLOCK_PADDING)
        self._paint_text(painter, content, block, is_current)
        painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        block = index.data(BLOCK_ROLE)
        card_width = self._row_layout(option.rect).card_width
        key = (block.id, card_width)
        if key not in self._card_heights:
            self._card_heights[key] = self._card_height(block, index.row(), card_width)
        return QSize(card_width, self._card_heights[key] + theme.BLOCK_SPACING)

    @staticmethod
    def _paint_card(painter: QPainter, card: QRect, is_current: bool) -> None:
        painter.setBrush(theme.CURRENT_BLOCK if is_current else theme.BLOCK)
        if is_current:
            painter.setPen(QPen(theme.CURRENT_MARKER, theme.CURRENT_BORDER_WIDTH))
            outline = QRectF(card).adjusted(1, 1, -1, -1)
        else:
            painter.setPen(Qt.NoPen)
            outline = QRectF(card)
        painter.drawRoundedRect(outline, theme.BLOCK_CORNER_RADIUS, theme.BLOCK_CORNER_RADIUS)

    def _paint_text(self, painter: QPainter, content: QRect, block: Block, is_current: bool) -> None:
        document = self._text_document(block, content.width(), is_current)
        painter.save()
        painter.translate(content.topLeft())
        document.drawContents(painter)
        painter.restore()

    def _card_height(self, block: Block, row: int, card_width: int) -> int:
        text_width = card_width - 2 * theme.BLOCK_PADDING
        text_height = self._text_document(block, text_width, is_current=False).size().height()
        label_height = max((CueStyle.cue_label_height(len(segment.details))
                            for segment in self._cue_lanes.starting_at(row, self._visible_lanes)), default=0)
        return math.ceil(max(text_height, label_height)) + 2 * theme.BLOCK_PADDING

    def _row_layout(self, row: QRect) -> RowLayout:
        return RowLayout(row.x(), row.width() or self._viewport_width, self._visible_lanes)

    @staticmethod
    def _text_document(block: Block, width: int, is_current: bool) -> QTextDocument:
        document = QTextDocument()
        document.setDocumentMargin(0)
        document.setHtml(_block_html(block, is_current))
        document.setTextWidth(width)
        return document


def _block_html(block: Block, is_current: bool) -> str:
    """The left column of a block: the character name above its text, as rich text."""
    paragraphs = []
    if block.character:
        color = theme.CHARACTER if is_current else theme.DIMMED_CHARACTER
        paragraphs.append(f'<p style="margin:0 0 4px 0; font-size:{theme.CHARACTER_POINT_SIZE}pt; '
                          f'color:{color.name()}"><b>{html.escape(block.character.upper())}</b></p>')
    text = _text_html(block, is_current)
    if text:
        paragraphs.append(f'<p style="margin:0; font-size:{theme.FONT_POINT_SIZE}pt">{text}</p>')
    return "".join(paragraphs) or "&nbsp;"


def _text_html(block: Block, is_current: bool) -> str:
    """The stage direction in brackets followed by the text of the block."""
    parts = []
    if block.direction:
        color = theme.DIRECTION_TEXT if is_current else theme.DIMMED_DIRECTION_TEXT
        parts.append(f'<i style="color:{color.name()}">({html.escape(block.direction)})</i>')
    if block.text:
        parts.append(f'<span style="color:{_text_color(block, is_current).name()}">'
                     f'{_emphasized(html.escape(block.text), block.type)}</span>')
    return " ".join(parts)


def _text_color(block: Block, is_current: bool) -> QColor:
    if block.type == "command":
        return theme.COMMAND_TEXT if is_current else theme.DIMMED_COMMAND_TEXT
    return theme.TEXT if is_current else theme.DIMMED_TEXT


def _emphasized(text: str, block_type: str) -> str:
    if block_type == "command":
        return f"<b>{text}</b>"
    if block_type == "acting":
        return f"<i>{text}</i>"
    return text

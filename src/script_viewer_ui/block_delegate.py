import html
import math
from dataclasses import dataclass

from PyQt5.QtCore import QModelIndex, QRect, QRectF, QSize, Qt
from PyQt5.QtGui import QColor, QFont, QFontMetrics, QPainter, QPen, QTextDocument
from PyQt5.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem

from model.block import Block
from script_viewer_ui import theme
from script_viewer_ui.block_list_model import BLOCK_ROLE, IS_CURRENT_ROLE, LANE_LINES_ROLE
from script_viewer_ui.cue_lanes import LANES, CueLane
from script_viewer_ui.row_layout import RowLayout

UNMUTE_PREFIX = "▲ "
MUTE_PREFIX = "▼ "
AUDIO_PREFIX = "♪ "
LIGHT_PREFIX = "☀ "


@dataclass(frozen=True)
class _Columns:
    """Widths of the two columns of a block card."""

    text: int
    cues: int


class BlockDelegate(QStyledItemDelegate):
    """Paints one block as a card of a document: character and text left, cues right, cue lanes beside.

    The left column of the card holds the character name above its spoken text
    or stage direction, the right column holds the mic, audio and light cues of
    the block. Right of the card, the LiSP cues, X32 snippets and light cues
    generated for the block are listed in their colored lanes, which are tinted
    over the full height of the row, so they run down the page uninterrupted.
    The current block is drawn in white on a lighter card with a border, every
    other block is dimmed.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._viewport_width = 0
        self._card_heights: dict[tuple[int, int], int] = {}

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
        lane_lines = index.data(LANE_LINES_ROLE)
        layout = self._row_layout(option.rect)
        card = layout.card_rect(option.rect.y(), option.rect.height() - theme.BLOCK_SPACING)
        columns = self._columns(card.width())

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)
        self._paint_lanes(painter, layout, option.rect, lane_lines, is_current)
        self._paint_card(painter, card, is_current)

        content = card.adjusted(theme.BLOCK_PADDING, theme.BLOCK_PADDING, -theme.BLOCK_PADDING, -theme.BLOCK_PADDING)
        self._paint_text(painter, content, columns, block, is_current)
        self._paint_cues(painter, content, columns, block, is_current)
        painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        block = index.data(BLOCK_ROLE)
        lane_lines = index.data(LANE_LINES_ROLE)
        card_width = self._row_layout(option.rect).card_width
        key = (block.id, card_width)
        if key not in self._card_heights:
            self._card_heights[key] = self._card_height(block, lane_lines, card_width)
        return QSize(card_width, self._card_heights[key] + theme.BLOCK_SPACING)

    @staticmethod
    def _paint_card(painter: QPainter, card: QRect, is_current: bool) -> None:
        painter.setBrush(theme.CURRENT_BLOCK if is_current else theme.BLOCK)
        if is_current:
            painter.setPen(QPen(theme.CURRENT_MARKER, theme.CURRENT_BORDER_WIDTH))
            # The pen is centered on the outline, so the rect is inset by half its width.
            outline = QRectF(card).adjusted(1, 1, -1, -1)
        else:
            painter.setPen(Qt.NoPen)
            outline = QRectF(card)
        painter.drawRoundedRect(outline, theme.BLOCK_CORNER_RADIUS, theme.BLOCK_CORNER_RADIUS)

    def _paint_lanes(self, painter: QPainter, layout: RowLayout, row: QRect,
                     lane_lines: tuple[list[str], ...], is_current: bool) -> None:
        font = self._lane_font()
        painter.setFont(font)
        metrics = QFontMetrics(font)
        for lane_index, (lane, lines) in enumerate(zip(LANES, lane_lines)):
            lane_rect = layout.lane_rect(lane_index, row.y(), row.height())
            self._paint_lane_background(painter, lane_rect, lane)

            line = QRect(lane_rect.x() + theme.LANE_LABEL_PADDING, row.y() + theme.BLOCK_PADDING,
                         lane_rect.width() - 2 * theme.LANE_LABEL_PADDING, metrics.lineSpacing())
            painter.setPen(lane.color if is_current else lane.dimmed_color)
            for text in lines:
                painter.drawText(line, Qt.AlignLeft | Qt.AlignVCenter, metrics.elidedText(text, Qt.ElideMiddle, line.width()))
                line.translate(0, metrics.lineSpacing())

    @staticmethod
    def _paint_lane_background(painter: QPainter, lane_rect: QRect, lane: CueLane) -> None:
        tint = QColor(lane.color)
        tint.setAlpha(theme.LANE_TINT_ALPHA)
        painter.fillRect(lane_rect, tint)
        edge = QColor(lane.color)
        edge.setAlpha(theme.LANE_EDGE_ALPHA)
        painter.fillRect(QRect(lane_rect.x(), lane_rect.y(), 2, lane_rect.height()), edge)

    def _paint_text(self, painter: QPainter, content: QRect, columns: _Columns, block: Block, is_current: bool) -> None:
        document = self._text_document(block, columns.text, is_current)
        painter.save()
        painter.translate(content.topLeft())
        document.drawContents(painter)
        painter.restore()

    def _paint_cues(self, painter: QPainter, content: QRect, columns: _Columns, block: Block, is_current: bool) -> None:
        font = self._cue_font()
        painter.setFont(font)
        line_height = QFontMetrics(font).lineSpacing()

        line = QRect(content.right() - columns.cues, content.top(), columns.cues, line_height)
        for text, color in self._cue_lines(block, is_current):
            painter.setPen(color)
            painter.drawText(line, Qt.AlignLeft | Qt.AlignVCenter, text)
            line.translate(0, line_height)

    def _card_height(self, block: Block, lane_lines: tuple[list[str], ...], card_width: int) -> int:
        columns = self._columns(card_width)
        text_height = self._text_document(block, columns.text, is_current=False).size().height()
        cue_height = len(self._cue_lines(block, is_current=False)) * QFontMetrics(self._cue_font()).lineSpacing()
        lane_height = max(len(lines) for lines in lane_lines) * QFontMetrics(self._lane_font()).lineSpacing()
        return math.ceil(max(text_height, cue_height, lane_height)) + 2 * theme.BLOCK_PADDING

    def _row_layout(self, row: QRect) -> RowLayout:
        return RowLayout(row.x(), row.width() or self._viewport_width)

    @staticmethod
    def _columns(card_width: int) -> _Columns:
        inner = card_width - 2 * theme.BLOCK_PADDING
        cues = min(theme.CUE_COLUMN_WIDTH, inner // 3)
        return _Columns(text=inner - cues - theme.COLUMN_GAP, cues=cues)

    @staticmethod
    def _text_document(block: Block, width: int, is_current: bool) -> QTextDocument:
        document = QTextDocument()
        document.setDocumentMargin(0)
        document.setHtml(_block_html(block, is_current))
        document.setTextWidth(width)
        return document

    @staticmethod
    def _cue_lines(block: Block, is_current: bool) -> list[tuple[str, QColor]]:
        lines = [(UNMUTE_PREFIX + name, theme.UNMUTE if is_current else theme.DIMMED_UNMUTE) for name in block.unmute]
        lines += [(MUTE_PREFIX + name, theme.MUTE if is_current else theme.DIMMED_MUTE) for name in block.mute]
        if block.audio_effect:
            lines.append((AUDIO_PREFIX + block.audio_effect,
                          theme.AUDIO_EFFECT if is_current else theme.DIMMED_AUDIO_EFFECT))
        if block.light:
            lines.append((LIGHT_PREFIX + block.light, theme.LIGHT if is_current else theme.DIMMED_LIGHT))
        return lines

    @staticmethod
    def _cue_font() -> QFont:
        font = QFont()
        font.setPointSize(theme.CUE_POINT_SIZE)
        font.setBold(True)
        return font

    @staticmethod
    def _lane_font() -> QFont:
        font = QFont()
        font.setPointSize(theme.LANE_POINT_SIZE)
        return font


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

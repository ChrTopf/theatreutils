from PyQt5.QtCore import QRect

from script_viewer_ui import theme
from script_viewer_ui.cue_lanes import LANES

# The narrowest block card that is still readable, used if the window is tiny.
MIN_CARD_WIDTH = 320

LANES_WIDTH = len(LANES) * theme.LANE_WIDTH + (len(LANES) - 1) * theme.LANE_GAP


class RowLayout:
    """Horizontal geometry of a row of the document: the block card followed by the cue lanes.

    The card and the lanes are centered on the page together. Both the
    BlockDelegate painting the rows and the BlockListView painting the lane
    names use this layout, so the names always sit on top of their lanes.
    """

    def __init__(self, row_left: int, row_width: int):
        available = row_width - 2 * theme.PAGE_MARGIN - theme.COLUMN_GAP - LANES_WIDTH
        self.card_width = max(MIN_CARD_WIDTH, min(available, theme.MAX_CONTENT_WIDTH))
        content_width = self.card_width + theme.COLUMN_GAP + LANES_WIDTH
        self.card_left = row_left + max(theme.PAGE_MARGIN, (row_width - content_width) // 2)

    def card_rect(self, top: int, height: int) -> QRect:
        return QRect(self.card_left, top, self.card_width, height)

    def lane_rect(self, lane_index: int, top: int, height: int) -> QRect:
        left = self.card_left + self.card_width + theme.COLUMN_GAP + lane_index * (theme.LANE_WIDTH + theme.LANE_GAP)
        return QRect(left, top, theme.LANE_WIDTH, height)

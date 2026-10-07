from PyQt5.QtCore import QRect

from script_viewer_ui import theme
from script_viewer_ui.cue_lanes import CueLane

# The narrowest block card that is still readable, used if the window is tiny.
MIN_CARD_WIDTH = 320


class RowLayout:
    """Horizontal geometry of a row of the document: the block card followed by the visible cue lanes.

    The card and the lanes are centered on the page together. Hidden lanes take
    no space, so the card grows into it. The BlockDelegate painting the rows,
    the BlockListView painting the cue lanes and the CueLaneHeader painting the
    lane names all use this layout, so the names always sit on top of their lanes.
    """

    def __init__(self, row_left: int, row_width: int, lanes: tuple[CueLane, ...]):
        self.lanes = lanes
        lanes_width = len(lanes) * theme.LANE_WIDTH + max(len(lanes) - 1, 0) * theme.LANE_GAP
        lanes_space = theme.COLUMN_GAP + lanes_width if lanes else 0

        available = row_width - 2 * theme.PAGE_MARGIN - lanes_space
        self.card_width = max(MIN_CARD_WIDTH, min(available, theme.MAX_CONTENT_WIDTH))
        content_width = self.card_width + lanes_space
        self.card_left = row_left + max(theme.PAGE_MARGIN, (row_width - content_width) // 2)

    def card_rect(self, top: int, height: int) -> QRect:
        return QRect(self.card_left, top, self.card_width, height)

    def lane_rect(self, lane: CueLane, top: int, height: int) -> QRect:
        position = self.lanes.index(lane)
        left = self.card_left + self.card_width + theme.COLUMN_GAP + position * (theme.LANE_WIDTH + theme.LANE_GAP)
        return QRect(left, top, theme.LANE_WIDTH, height)

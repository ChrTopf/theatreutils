from PyQt5.QtCore import QRect

from script_viewer_ui import theme
from script_viewer_ui.cue_lane_segments import CueLane

MIN_CARD_WIDTH = 320


class RowLayout:
    """Horizontal geometry of a row of the document: the block card followed by the visible cue lanes."""

    def __init__(self, row_left: int, row_width: int, lanes: tuple[CueLane, ...], lane_width: int):
        self.lanes = lanes
        self.lane_width = lane_width
        lanes_width = len(lanes) * lane_width + max(len(lanes) - 1, 0) * theme.LANE_GAP
        lanes_space = theme.COLUMN_GAP + lanes_width if lanes else 0

        available = row_width - 2 * theme.PAGE_MARGIN - lanes_space
        self.card_width = max(MIN_CARD_WIDTH, min(available, theme.MAX_CONTENT_WIDTH))
        content_width = self.card_width + lanes_space
        self.card_left = row_left + max(theme.PAGE_MARGIN, (row_width - content_width) // 2)

    def card_rect(self, top: int, height: int) -> QRect:
        return QRect(self.card_left, top, self.card_width, height)

    def lane_rect(self, lane: CueLane, top: int, height: int) -> QRect:
        position = self.lanes.index(lane)
        left = self.card_left + self.card_width + theme.COLUMN_GAP + position * (self.lane_width + theme.LANE_GAP)
        return QRect(left, top, self.lane_width, height)

from PyQt5.QtGui import QFont, QFontMetrics

from script_viewer_ui import theme

class CueStyle:
    @staticmethod
    def cue_name_font() -> QFont:
        font = QFont()
        font.setPointSize(theme.LANE_POINT_SIZE)
        font.setBold(True)
        return font

    @staticmethod
    def cue_location_font() -> QFont:
        font = QFont()
        font.setPointSize(theme.CUE_LOCATION_POINT_SIZE)
        return font

    @staticmethod
    def cue_label_height(name_count: int) -> int:
        if name_count == 0:
            return 0
        return name_count * QFontMetrics(CueStyle.cue_name_font()).lineSpacing() + QFontMetrics(CueStyle.cue_location_font()).lineSpacing()
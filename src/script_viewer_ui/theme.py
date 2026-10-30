"""Colors, fonts and metrics of the Script Viewer.

The viewer is used backstage during the live show, so it looks like a document
reader on a dark page: every block is a card, and all cards except the current
one are dimmed, so the eye always finds its way back to where the show is.
"""

from PyQt5.QtGui import QColor

FONT_POINT_SIZE = 14
CHARACTER_POINT_SIZE = 12
CUE_POINT_SIZE = 12
STATUS_POINT_SIZE = 11
LANE_POINT_SIZE = 18
CUE_LOCATION_POINT_SIZE = 14
LANE_LABEL_POINT_SIZE = 10

# Geometry of a block card, in pixels.
MAX_CONTENT_WIDTH = 1200
PAGE_MARGIN = 24
BLOCK_SPACING = 6
BLOCK_PADDING = 14
CURRENT_BORDER_WIDTH = 2
BLOCK_CORNER_RADIUS = 6
CUE_COLUMN_WIDTH = 230
COLUMN_GAP = 24

# Geometry of the cue lanes running down the page right of the block cards, in pixels.
# Wide enough for the cue names below the labels, e.g. "1. Akt S12 B415".
LANE_WIDTH = 300
LANE_GAP = 8
LANE_LABEL_MARGIN = 8
LANE_LABEL_PADDING = 8
CUE_BAR_WIDTH = 4
# How far a cue name keeps away from the upper edge of the view while it sticks to it.
CUE_NAME_STICKY_MARGIN = 6

# The page the block cards lie on.
PAGE = QColor("#0d0d0f")
BLOCK = QColor("#16161a")
CURRENT_BLOCK = QColor("#20242e")
CURRENT_MARKER = QColor("#9ec1ff")

TEXT = QColor("#ffffff")
DIMMED_TEXT = QColor("#63636b")

CHARACTER = QColor("#9ec1ff")
DIMMED_CHARACTER = QColor("#4a5a75")

COMMAND_TEXT = QColor("#ffb074")
DIMMED_COMMAND_TEXT = QColor("#7a5536")

DIRECTION_TEXT = QColor("#c9c9d2")
DIMMED_DIRECTION_TEXT = QColor("#55555d")

MUTE = QColor("#ff5c5c")
DIMMED_MUTE = QColor("#7e3a3a")
UNMUTE = QColor("#5cdc7a")
DIMMED_UNMUTE = QColor("#36704a")

AUDIO_EFFECT = QColor("#5cc8ff")
DIMMED_AUDIO_EFFECT = QColor("#356079")
LIGHT = QColor("#ffe066")
DIMMED_LIGHT = QColor("#7d7039")

# The cue lanes: the color of the lane name in the header. The X32 and light cues are drawn in their lane's color,
# the LiSP cues in the colors they have in LiSP.
LISP_LANE = QColor("#c39bff")
X32_LANE = QColor("#4fd8c4")
LIGHT_CUE_LANE = QColor("#ffb84d")
LANE_LABEL_BACKGROUND = QColor(13, 13, 15, 235)

# Cues that are not active at the current block are darkened by this factor, see QColor.darker().
DIMMED_CUE_FACTOR = 220

# The bar above the page holding the scene navigation and the position.
BAR = QColor("#16161a")
BAR_BORDER = QColor("#26262c")
MUTED_LABEL = QColor("#8c8c96")

SCROLLBAR_HANDLE = QColor("#3a3a44")
SCROLLBAR_HANDLE_HOVER = QColor("#4f4f5c")

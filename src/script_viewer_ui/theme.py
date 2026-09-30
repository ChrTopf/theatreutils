"""Colors and fonts of the Script Viewer.

The viewer is used backstage during the live show, so it uses a dark theme
that does not light up the surroundings. Every block except the current one
is dimmed, so the eye always finds its way back to where the show is.
"""

from PyQt5.QtGui import QColor

FONT_POINT_SIZE = 14

BACKGROUND = QColor("#121212")
CURRENT_BACKGROUND = QColor("#2b3a55")
GRID = QColor("#2a2a2a")

TEXT = QColor("#f0f0f0")
DIMMED_TEXT = QColor("#7a7a7a")

COMMAND_TEXT = QColor("#ff9e5e")
DIMMED_COMMAND_TEXT = QColor("#8a5a3a")

MUTE = QColor("#ff5c5c")
DIMMED_MUTE = QColor("#a04545")
UNMUTE = QColor("#5cdc7a")
DIMMED_UNMUTE = QColor("#3f8a52")

AUDIO_EFFECT = QColor("#5cc8ff")
DIMMED_AUDIO_EFFECT = QColor("#3f7a9a")
LIGHT = QColor("#ffe066")
DIMMED_LIGHT = QColor("#9a8a45")

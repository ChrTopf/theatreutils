from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Cue:
    """The line announcing that a character speaks, e.g. `Polizist: (kopfschüttelnd)`."""

    character: str
    direction: Optional[str]

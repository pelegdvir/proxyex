from enum import Enum, auto


class DetectorAction(Enum):
    """The short action that the detector recommends"""

    # Drop right away - this is EVIL
    Drop = auto()
    # Consider to warn the user that something bad is happening - but don't drop it
    Warn = auto()
    # This is fine, prb a god/debug mode. Do not ship to prod on a suite
    PassAll = auto()
    # A normal packet, might be fine / not. We might gave a grade to it.
    Continue = auto()

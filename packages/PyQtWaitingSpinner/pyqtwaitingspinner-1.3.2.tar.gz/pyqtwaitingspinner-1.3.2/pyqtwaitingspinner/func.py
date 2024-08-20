from pyqtwaitingspinner import msg
from pyqtwaitingspinner.enum import SpinDirection


def int_to_spin_direction(direction: int) -> SpinDirection:
    if direction < 0 or direction > (len(SpinDirection) - 1):
        raise ValueError(msg.INVALID_SPIN_DIRECTION)

    return SpinDirection(direction)

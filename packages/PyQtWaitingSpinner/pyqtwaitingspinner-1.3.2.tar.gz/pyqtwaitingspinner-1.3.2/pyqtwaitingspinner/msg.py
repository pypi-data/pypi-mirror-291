from pyqtwaitingspinner.enum import SpinDirection

# from enum import StrEnum


# class ErrorMessage(StrEnum):
#     INVALID_SPIN_DIRECTION = (
#         "spin_direction must be 0 or 1, or a value in the SpinDirection enum."  # noqa: E501
#     )

_spin_direction_len: int = len(SpinDirection)

INVALID_SPIN_DIRECTION: str = (
    "Spin direction must be between 0 and "
    f"{_spin_direction_len}, or a value in the SpinDirection enum."
)

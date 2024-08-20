from enum import IntEnum


class SpinDirection(IntEnum):
    CLOCKWISE = 0
    COUNTERCLOCKWISE = 1
    # will require a bit more than just 'signing' the "rotate_angle"
    # variable in "paintEvent"
    # PINGPONG = 2

    def __str__(self) -> str:
        return self.name

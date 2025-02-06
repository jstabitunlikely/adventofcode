from __future__ import annotations
from typing import Optional

from Coordinate import Coordinate


class Wall(Coordinate):

    def push(self, dir: str) -> bool:
        return False

    def nudge(self, dir: str) -> bool:
        return False

    def __repr__(self):
        return repr('#')


class Space(Coordinate):

    def push(self, dir: str) -> bool:
        return True

    def nudge(self, dir: str) -> bool:
        return True

    def __repr__(self):
        return repr('.')


class Box(Coordinate):

    other_half: Optional[Box] = None

    def __init__(self,
                 x: int,
                 y: int,
                 is_left_half: bool,
                 warehouse: list[list]):
        super().__init__(x, y)
        self.warehouse = warehouse
        self.is_left_half = is_left_half
        # This flag prevents left and right halves infinitely nudging each other.
        self.is_nudge_in_progress = False

    def move(self, direction: str) -> bool:
        nx = self.x + self.COMPASS[direction][0]
        ny = self.y + self.COMPASS[direction][1]
        if p := self.warehouse[nx][ny].push(direction):
            self.warehouse[nx][ny] = self
            self.warehouse[self.x][self.y] = Space(self.x, self.y)
            self.x = nx
            self.y = ny
        return p

    def push(self, direction: str) -> bool:
        # Horizontal push is nothing special
        if direction in '<>':
            return self.move(direction)
        # Vertical push needs to handle both halves
        elif p := self.nudge(direction):
            if self.other_half is not None:
                self.other_half.move(direction)
            self.move(direction)
        return p

    def nudge(self, direction: str) -> bool:
        self.is_nudge_in_progress = True
        nx = self.x + self.COMPASS[direction][0]
        ny = self.y + self.COMPASS[direction][1]
        ok = self.warehouse[nx][ny].nudge(direction)
        if self.other_half is not None and not self.other_half.is_nudge_in_progress:
            ok &= self.other_half.nudge(direction)
        self.is_nudge_in_progress = False
        return ok

    def __repr__(self):
        if self.other_half is None:
            return repr('O')
        elif self.is_left_half:
            return repr('[')
        else:
            return repr(']')


class Robot(Box):

    def __init__(self,
                 x: int,
                 y: int,
                 warehouse: list[list]):
        super().__init__(x, y, is_left_half=False, warehouse=warehouse)

    def __repr__(self):
        return repr('@')

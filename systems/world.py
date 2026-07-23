"""The world map: which room CSV sits at each grid coordinate."""


class World:
    """A grid of rooms and the coordinate currently being played.

    Connectivity is implicit in the grid: the room to the right of (gx, gy)
    is whatever lives at (gx + 1, gy). If that cell isn't in ROOMS, there's
    no room that way — so "does the neighbor cell exist?" is the entire
    adjacency rule, and the map is authored as a plain dict.

        (0,0) room_0 ── right ── (1,0) room_1
           │
          down
           │
        (0,1) room_2
    """

    ROOMS = {
        (0, 0): "room_0.csv",
        (1, 0): "room_1.csv",
        (0, 1): "room_2.csv",
    }
    START = (0, 0)

    def __init__(self) -> None:
        self.coord = self.START

    def file_for(self, coord: tuple[int, int]) -> str:
        return self.ROOMS[coord]

    def neighbor(self, direction: tuple[int, int]) -> tuple[int, int] | None:
        """The coordinate one step in `direction`, or None if no room is there."""
        target = (self.coord[0] + direction[0], self.coord[1] + direction[1])
        return target if target in self.ROOMS else None

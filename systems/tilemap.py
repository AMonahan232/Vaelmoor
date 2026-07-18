"""CSV-backed room tilemap."""

import csv
from pathlib import Path

import pygame

from config import TILE_SIZE, COLOR_FLOOR, COLOR_WALL

# Tile ids as they appear in the CSV files
FLOOR = 0
WALL = 1


class Tilemap:
    """A single room loaded from a CSV grid of tile ids.

    The room is drawn once onto ``self.surface`` at load time, so rendering
    each frame is a single blit instead of ~600 per-tile draws. Wall tiles
    are also collected into ``self.solids`` for collision checks.
    """

    def __init__(self, csv_path: str | Path) -> None:
        with open(csv_path, newline="") as f:
            self.grid = [[int(cell) for cell in row] for row in csv.reader(f)]
        self.height = len(self.grid)
        self.width = len(self.grid[0])

        self.solids = [
            pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            for row, line in enumerate(self.grid)
            for col, tile in enumerate(line)
            if tile == WALL
        ]

        self.surface = pygame.Surface(
            (self.width * TILE_SIZE, self.height * TILE_SIZE)
        )
        for row, line in enumerate(self.grid):
            for col, tile in enumerate(line):
                color = COLOR_WALL if tile == WALL else COLOR_FLOOR
                pygame.draw.rect(
                    self.surface,
                    color,
                    (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                )

    def is_solid(self, col: int, row: int) -> bool:
        """Whether the tile at grid coordinates (col, row) blocks movement.

        Out-of-bounds counts as solid so nothing can walk off the map.
        """
        if not (0 <= col < self.width and 0 <= row < self.height):
            return True
        return self.grid[row][col] == WALL

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.surface, (0, 0))

"""The player character."""

import pygame

from config import TILE_SIZE, PLAYER_SPEED, COLOR_PLAYER
from entities.entity import Entity


class Player(Entity):
    """Top-down player: reads held keys each frame and moves in 8 directions."""

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, TILE_SIZE, COLOR_PLAYER)

    def update(self, dt: float, solids: list[pygame.Rect]) -> None:
        keys = pygame.key.get_pressed()
        direction = pygame.math.Vector2(
            (keys[pygame.K_RIGHT] or keys[pygame.K_d])
            - (keys[pygame.K_LEFT] or keys[pygame.K_a]),
            (keys[pygame.K_DOWN] or keys[pygame.K_s])
            - (keys[pygame.K_UP] or keys[pygame.K_w]),
        )
        if direction.length_squared() > 0:
            # Normalize so diagonal movement isn't ~41% faster than straight
            direction = direction.normalize()
            self.facing = direction

        self._move_axis(direction.x * PLAYER_SPEED * dt, 0, solids)
        self._move_axis(0, direction.y * PLAYER_SPEED * dt, solids)

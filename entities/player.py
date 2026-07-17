"""The player character."""

import pygame

from config import TILE_SIZE, PLAYER_SPEED, COLOR_PLAYER


class Player(pygame.sprite.Sprite):
    """Top-down player: reads held keys each frame and moves in 8 directions.

    Position is tracked in a float Vector2 separate from ``rect`` because
    rects only store integers — moving 2.5px/frame through a rect alone
    would round away half the movement.
    """

    def __init__(self, x: float, y: float) -> None:
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(COLOR_PLAYER)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos = pygame.math.Vector2(x, y)
        # Facing matters later for sword swings and dialogue triggers
        self.facing = pygame.math.Vector2(0, 1)

    def update(self, dt: float) -> None:
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

        self.pos += direction * PLAYER_SPEED * dt
        self.rect.topleft = round(self.pos.x), round(self.pos.y)

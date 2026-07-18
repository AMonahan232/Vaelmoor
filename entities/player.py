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

        # Move one axis at a time so hitting a wall diagonally still lets
        # the free axis slide along it instead of stopping dead.
        self._move_axis(direction.x * PLAYER_SPEED * dt, 0, solids)
        self._move_axis(0, direction.y * PLAYER_SPEED * dt, solids)

    def _move_axis(self, dx: float, dy: float, solids: list[pygame.Rect]) -> None:
        self.pos.x += dx
        self.pos.y += dy
        self.rect.topleft = round(self.pos.x), round(self.pos.y)

        for index in self.rect.collidelistall(solids):
            wall = solids[index]
            if dx > 0:
                self.rect.right = wall.left
            elif dx < 0:
                self.rect.left = wall.right
            if dy > 0:
                self.rect.bottom = wall.top
            elif dy < 0:
                self.rect.top = wall.bottom
            # Snap the float position to the resolved rect so sub-pixel
            # error can't accumulate and tunnel us into the wall later
            self.pos.update(self.rect.topleft)

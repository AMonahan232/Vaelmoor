"""Shared base class for anything that moves and collides with the map."""

import pygame


class Entity(pygame.sprite.Sprite):
    """A movable sprite with float-precision position and wall collision.

    Position is tracked in a float Vector2 separate from ``rect`` because
    rects only store integers — moving 2.5px/frame through a rect alone
    would round away half the movement.
    """

    def __init__(
        self, x: float, y: float, size: int, color: tuple[int, int, int]
    ) -> None:
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos = pygame.math.Vector2(x, y)
        self.facing = pygame.math.Vector2(0, 1)

    def _move_axis(
        self, dx: float, dy: float, solids: list[pygame.Rect]
    ) -> bool:
        """Move along one axis, resolving overlaps against solid tiles.

        Callers move one axis at a time so hitting a wall diagonally still
        lets the free axis slide along it. Returns True if a wall was hit,
        which AI (turn around) and future knockback code can react to.
        """
        self.pos.x += dx
        self.pos.y += dy
        self.rect.topleft = round(self.pos.x), round(self.pos.y)

        collided = False
        for index in self.rect.collidelistall(solids):
            wall = solids[index]
            collided = True
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
        return collided

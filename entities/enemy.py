"""A wandering enemy."""

import random

import pygame

from config import (
    TILE_SIZE,
    ENEMY_SPEED,
    ENEMY_WALK_TIME,
    ENEMY_IDLE_TIME,
    ENEMY_HEALTH,
    KNOCKBACK_SPEED,
    KNOCKBACK_TIME,
    COLOR_ENEMY,
    COLOR_ENEMY_HURT,
)
from entities.entity import Entity

CARDINALS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

# Module-level RNG used by the real game; tests pass their own seeded
# random.Random so enemy behavior is reproducible in assertions.
_rng = random.Random()


class Enemy(Entity):
    """Octorok-style wanderer: walk a random cardinal direction, then pause.

    Behavior is a two-state machine (WALK/IDLE) driven by countdown timers.
    Hitting a wall ends a walk early. States instead of nested ifs because
    later behaviors (chase, flee, attack) then become new states rather
    than deeper conditionals.
    """

    def __init__(self, x: float, y: float, rng: random.Random = _rng) -> None:
        super().__init__(x, y, TILE_SIZE, COLOR_ENEMY)
        self.rng = rng
        self.direction = pygame.math.Vector2()
        self.health = ENEMY_HEALTH
        self.knock_dir = pygame.math.Vector2()
        self.state = "idle"
        self.timer = rng.uniform(*ENEMY_IDLE_TIME)

    def take_hit(self, direction: pygame.math.Vector2) -> None:
        """Take one sword hit: die at 0 HP, otherwise get knocked back."""
        self.health -= 1
        if self.health <= 0:
            self.kill()  # drops us out of every sprite group
            return
        self.state = "hurt"
        self.timer = KNOCKBACK_TIME
        self.knock_dir = pygame.math.Vector2(direction)
        if self.knock_dir.length_squared() > 0:
            self.knock_dir = self.knock_dir.normalize()
        self.image.fill(COLOR_ENEMY_HURT)

    def update(self, dt: float, solids: list[pygame.Rect]) -> None:
        self.timer -= dt
        if self.state == "hurt":
            # _move_axis resolves against walls, so knockback can't
            # shove an enemy through them
            self._move_axis(self.knock_dir.x * KNOCKBACK_SPEED * dt, 0, solids)
            self._move_axis(0, self.knock_dir.y * KNOCKBACK_SPEED * dt, solids)
            if self.timer <= 0:
                self.image.fill(COLOR_ENEMY)
                self._enter_idle()
        elif self.state == "walk":
            hit_wall = self._move_axis(self.direction.x * ENEMY_SPEED * dt, 0, solids)
            hit_wall |= self._move_axis(0, self.direction.y * ENEMY_SPEED * dt, solids)
            if hit_wall or self.timer <= 0:
                self._enter_idle()
        elif self.timer <= 0:
            self._enter_walk()

    def _enter_idle(self) -> None:
        self.state = "idle"
        self.timer = self.rng.uniform(*ENEMY_IDLE_TIME)

    def _enter_walk(self) -> None:
        self.state = "walk"
        self.timer = self.rng.uniform(*ENEMY_WALK_TIME)
        self.direction = pygame.math.Vector2(self.rng.choice(CARDINALS))
        self.facing = self.direction.copy()

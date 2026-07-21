"""Tests for the wandering enemy AI (seeded RNG keeps them deterministic)."""

import random

import pygame
import pytest

from config import MAPS_DIR, TILE_SIZE
from entities.enemy import Enemy
from systems.tilemap import Tilemap

DT = 1 / 60


@pytest.fixture()
def room():
    return Tilemap(MAPS_DIR / "room_0.csv")


def test_alternates_between_idle_and_walk():
    enemy = Enemy(160, 160, rng=random.Random(1))
    seen = set()
    for _ in range(600):  # 10 simulated seconds, plenty for both states
        enemy.update(DT, [])
        seen.add(enemy.state)
    assert seen == {"idle", "walk"}


def test_walking_moves_and_sets_facing():
    enemy = Enemy(160, 160, rng=random.Random(1))
    start = enemy.pos.copy()
    for _ in range(600):
        enemy.update(DT, [])
    assert enemy.pos != start
    assert enemy.facing.length() == 1


def test_wall_hit_ends_walk_early(room):
    # Start touching the left border wall, then force a walk straight into it
    enemy = Enemy(TILE_SIZE, TILE_SIZE * 5, rng=random.Random(2))
    enemy.state = "walk"
    enemy.timer = 99.0
    enemy.direction = pygame.math.Vector2(-1, 0)

    enemy.update(DT, room.solids)

    assert enemy.state == "idle", "hitting a wall should end the walk"
    assert enemy.rect.left == TILE_SIZE, "enemy should be flush against the wall"


def test_long_wander_never_enters_walls(room):
    rng = random.Random(3)
    enemies = [Enemy(x, y, rng=rng) for x, y in room.enemy_spawns]
    for _ in range(2000):  # ~33 simulated seconds
        for enemy in enemies:
            enemy.update(DT, room.solids)
    for enemy in enemies:
        assert enemy.rect.collidelistall(room.solids) == []

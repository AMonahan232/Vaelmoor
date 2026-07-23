"""Tests for sword combat: swing timing, hitbox, knockback, and death."""

import random

import pygame
import pytest

from config import (
    MAPS_DIR,
    TILE_SIZE,
    ENEMY_HEALTH,
    ATTACK_DURATION,
)
from entities.enemy import Enemy
from entities.player import Player
from systems.tilemap import Tilemap

DT = 1 / 60


class NoKeys:
    def __getitem__(self, key):
        return False


@pytest.fixture(autouse=True)
def no_keys_held(monkeypatch):
    """Player.update polls the keyboard; fake an idle one for tests."""
    monkeypatch.setattr(pygame.key, "get_pressed", lambda: NoKeys())


@pytest.fixture()
def room():
    return Tilemap(MAPS_DIR / "room_0.csv")


def make_enemy(x, y):
    return Enemy(x, y, rng=random.Random(1))


def test_hitbox_projects_along_facing():
    player = Player(160, 160)
    player.start_attack()
    # Default facing is down
    assert player.sword_hitbox.centery == player.rect.centery + TILE_SIZE
    player.facing = pygame.math.Vector2(1, 0)
    assert player.sword_hitbox.centerx == player.rect.centerx + TILE_SIZE


def test_cooldown_blocks_immediate_reswing():
    player = Player(160, 160)
    player.start_attack()
    for _ in range(int(ATTACK_DURATION / DT) + 2):  # swing expires...
        player.update(DT, [])
    assert not player.attacking
    player.start_attack()  # ...but cooldown hasn't
    assert not player.attacking


def test_swing_hits_an_enemy_once():
    player = Player(160, 160)
    player.facing = pygame.math.Vector2(1, 0)
    enemy = make_enemy(160 + TILE_SIZE, 160)
    player.start_attack()
    player.strike([enemy])
    player.strike([enemy])  # same swing, later frame
    assert enemy.health == ENEMY_HEALTH - 1


def test_miss_leaves_enemy_untouched():
    player = Player(160, 160)
    player.facing = pygame.math.Vector2(0, -1)  # swing away from the enemy
    enemy = make_enemy(160 + TILE_SIZE * 4, 160)
    player.start_attack()
    player.strike([enemy])
    assert enemy.health == ENEMY_HEALTH


def test_hit_knocks_back_and_walls_stop_it(room):
    # Enemy one tile from the right border wall; knock it rightward.
    # Row 5 (not the rows 9-10 doorway gap) so a wall is actually there.
    enemy = make_enemy(TILE_SIZE * 27, TILE_SIZE * 5)
    enemy.take_hit(pygame.math.Vector2(1, 0))
    assert enemy.state == "hurt"
    for _ in range(30):
        enemy.update(DT, room.solids)
    assert enemy.rect.right == TILE_SIZE * 29, "wall should stop knockback"
    assert enemy.state in ("idle", "walk"), "hurt state should have ended"


def test_enemy_dies_after_enough_hits():
    enemy = make_enemy(160, 160)
    group = pygame.sprite.Group(enemy)
    for _ in range(ENEMY_HEALTH):
        enemy.take_hit(pygame.math.Vector2(1, 0))
    assert not enemy.alive()
    assert len(group) == 0

"""Tests for player contact damage, i-frames, knockback, and death."""

import pygame
import pytest

from config import (
    MAPS_DIR,
    TILE_SIZE,
    PLAYER_MAX_HEALTH,
    PLAYER_INVULN_TIME,
    PLAYER_KNOCK_TIME,
)
from entities.player import Player
from systems.tilemap import Tilemap

DT = 1 / 60


class NoKeys:
    def __getitem__(self, key):
        return False


@pytest.fixture(autouse=True)
def no_keys_held(monkeypatch):
    monkeypatch.setattr(pygame.key, "get_pressed", lambda: NoKeys())


@pytest.fixture()
def room():
    return Tilemap(MAPS_DIR / "room_0.csv")


def tick(player, frames, solids=()):
    for _ in range(frames):
        player.update(DT, list(solids))


def test_hit_decrements_health_and_starts_iframes():
    player = Player(160, 160)
    player.take_hit(pygame.math.Vector2(1, 0))
    assert player.health == PLAYER_MAX_HEALTH - 1
    assert player.invulnerable


def test_hits_during_iframes_are_ignored():
    player = Player(160, 160)
    player.take_hit(pygame.math.Vector2(1, 0))
    for _ in range(10):
        player.take_hit(pygame.math.Vector2(1, 0))
    assert player.health == PLAYER_MAX_HEALTH - 1


def test_second_hit_lands_after_iframes_expire():
    player = Player(160, 160)
    player.take_hit(pygame.math.Vector2(1, 0))
    tick(player, int(PLAYER_INVULN_TIME / DT) + 2)
    assert not player.invulnerable
    player.take_hit(pygame.math.Vector2(1, 0))
    assert player.health == PLAYER_MAX_HEALTH - 2


def test_knockback_moves_player_and_walls_stop_it(room):
    # One tile from the left border wall; get knocked left into it
    player = Player(TILE_SIZE * 2, TILE_SIZE * 10)
    player.take_hit(pygame.math.Vector2(-1, 0))
    tick(player, int(PLAYER_KNOCK_TIME / DT) + 2, room.solids)
    assert player.rect.left == TILE_SIZE, "wall should stop knockback"


def test_input_ignored_during_knockback(monkeypatch):
    # Hold "right" the whole time; during knockback (leftward) the player
    # must not respond to input.
    class RightHeld:
        def __getitem__(self, key):
            return key in (pygame.K_RIGHT, pygame.K_d)

    monkeypatch.setattr(pygame.key, "get_pressed", lambda: RightHeld())
    player = Player(300, 160)
    player.take_hit(pygame.math.Vector2(-1, 0))  # knocked left
    start_x = player.pos.x
    player.update(DT, [])
    assert player.pos.x < start_x, "player moved right despite knockback"


def test_health_can_reach_zero():
    player = Player(160, 160)
    for _ in range(PLAYER_MAX_HEALTH):
        player.take_hit(pygame.math.Vector2(1, 0))
        tick(player, int(PLAYER_INVULN_TIME / DT) + 2)
    assert player.health == 0

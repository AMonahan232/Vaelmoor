"""Tests for the CSV tilemap system."""

import pytest

from config import MAPS_DIR, GRID_WIDTH, GRID_HEIGHT, TILE_SIZE
from systems.tilemap import Tilemap, WALL


@pytest.fixture()
def room():
    return Tilemap(MAPS_DIR / "room_0.csv")


def test_room_matches_screen_grid(room):
    assert room.width == GRID_WIDTH
    assert room.height == GRID_HEIGHT


def test_every_wall_tile_gets_a_solid_rect(room):
    wall_count = sum(row.count(WALL) for row in room.grid)
    assert wall_count > 0
    assert len(room.solids) == wall_count


def test_solid_rects_align_to_tile_grid(room):
    for rect in room.solids:
        assert rect.width == TILE_SIZE and rect.height == TILE_SIZE
        assert rect.x % TILE_SIZE == 0 and rect.y % TILE_SIZE == 0


def test_border_is_solid_and_center_is_walkable(room):
    assert room.is_solid(0, 0)
    assert room.is_solid(room.width - 1, room.height - 1)
    assert not room.is_solid(room.width // 2, room.height // 2)


def test_out_of_bounds_counts_as_solid(room):
    assert room.is_solid(-1, 5)
    assert room.is_solid(5, room.height)

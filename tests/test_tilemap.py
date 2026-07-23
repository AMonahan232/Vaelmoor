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


def test_enemy_spawns_are_collected_and_walkable(room):
    assert len(room.enemy_spawns) == 3
    for x, y in room.enemy_spawns:
        assert x % TILE_SIZE == 0 and y % TILE_SIZE == 0
        assert not room.is_solid(x // TILE_SIZE, y // TILE_SIZE)


# Doorway bands, shared by neighboring rooms so repositioning lands on floor
DOOR_ROWS = (9, 10)   # left/right edges
DOOR_COLS = (14, 15)  # top/bottom edges


def test_all_rooms_load_at_screen_size():
    for name in ("room_0.csv", "room_1.csv", "room_2.csv"):
        room = Tilemap(MAPS_DIR / name)
        assert (room.width, room.height) == (GRID_WIDTH, GRID_HEIGHT)


def test_horizontal_doorway_aligns_between_room_0_and_room_1():
    room0 = Tilemap(MAPS_DIR / "room_0.csv")
    room1 = Tilemap(MAPS_DIR / "room_1.csv")
    for r in DOOR_ROWS:
        assert not room0.is_solid(room0.width - 1, r), "room_0 right gap blocked"
        assert not room1.is_solid(0, r), "room_1 left gap blocked"


def test_vertical_doorway_aligns_between_room_0_and_room_2():
    room0 = Tilemap(MAPS_DIR / "room_0.csv")
    room2 = Tilemap(MAPS_DIR / "room_2.csv")
    for c in DOOR_COLS:
        assert not room0.is_solid(c, room0.height - 1), "room_0 bottom gap blocked"
        assert not room2.is_solid(c, 0), "room_2 top gap blocked"


def test_non_doorway_border_stays_solid():
    # A border tile well away from any doorway band is still a wall
    room0 = Tilemap(MAPS_DIR / "room_0.csv")
    assert room0.is_solid(0, 3)                       # left edge, above the gap
    assert room0.is_solid(5, room0.height - 1)        # bottom edge, left of gap

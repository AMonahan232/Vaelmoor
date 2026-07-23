"""Tests for the room-grid world map."""

from systems.world import World


def test_starts_at_start_coord():
    world = World()
    assert world.coord == World.START
    assert world.file_for(world.coord) == "room_0.csv"


def test_neighbor_exists_toward_a_real_room():
    world = World()  # at (0, 0)
    assert world.neighbor((1, 0)) == (1, 0)   # room_1 is to the right
    assert world.neighbor((0, 1)) == (0, 1)   # room_2 is below


def test_neighbor_is_none_toward_empty_grid_cell():
    world = World()  # at (0, 0)
    assert world.neighbor((-1, 0)) is None    # nothing to the left
    assert world.neighbor((0, -1)) is None    # nothing above


def test_neighbor_is_relative_to_current_coord():
    world = World()
    world.coord = (1, 0)                       # pretend we're in room_1
    assert world.neighbor((-1, 0)) == (0, 0)   # room_0 back to the left
    assert world.neighbor((1, 0)) is None      # nothing further right

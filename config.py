"""Global constants for Vaelmoor.

Everything size/speed/color related lives here so gameplay tuning
never requires hunting through entity code.
"""

from pathlib import Path

# Anchored to this file so the game runs from any working directory
PROJECT_ROOT = Path(__file__).resolve().parent
MAPS_DIR = PROJECT_ROOT / "assets" / "maps"

# Tile grid — rooms are built on a 32x32px grid, so the screen size is
# expressed in tiles to guarantee rooms always fit exactly.
TILE_SIZE = 32
GRID_WIDTH = 30   # tiles per row
GRID_HEIGHT = 20  # tiles per column

SCREEN_WIDTH = TILE_SIZE * GRID_WIDTH    # 960
SCREEN_HEIGHT = TILE_SIZE * GRID_HEIGHT  # 640

FPS = 60

# Movement speeds are in pixels per second (not per frame) so gameplay
# feels identical even if the frame rate dips.
PLAYER_SPEED = 200

# Placeholder palette until real art exists
COLOR_BG = (24, 26, 33)
COLOR_PLAYER = (92, 179, 99)
COLOR_FLOOR = (54, 48, 65)
COLOR_WALL = (108, 96, 130)

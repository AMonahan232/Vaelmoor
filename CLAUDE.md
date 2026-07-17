# Vaelmoor

A top-down action-adventure game inspired by classic Zelda-style gameplay, built as a
learning project for Claude Code.

## Stack
- Python 3.11.9 (via pyenv)
- Pygame 2.6.1
- VS Code
- Git for version control

## Environment
- Always use `python` and `python -m pip` — never `python3` or `pip3`

## Architecture
- OOP structure: `Player`, `Enemy`, `Tilemap`, `DialogueBox`, `Inventory` classes
- CSV-based tilemap system (same pattern as Altimon)
- 32x32px tile grid, top-down camera
- Sword/melee combat with hitbox-based collision
- Room-based dungeon layout (no seamless overworld scrolling yet)

## Conventions
- Assets as separate PNG/SVG files, not embedded in code
- One class per file under a `entities/` or `systems/` folder
- Constants (tile size, screen dims, colors) live in a single `config.py`

## Commands
- `python main.py` — run the game
- `python -m pytest` — run tests (once added)

## Notes for Claude
- This project is a learning exercise in using Claude Code itself, so favor
  incremental, explainable changes over large one-shot generations
- Prefer Plan Mode for any multi-file feature before implementing
- Explain *why*, not just *what*, when introducing a new pattern

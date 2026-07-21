"""Heads-up display: hearts for player health."""

import pygame

from config import PLAYER_MAX_HEALTH, COLOR_HEART

HEART_SIZE = 20
HEART_GAP = 6
HUD_MARGIN = 12


class HUD:
    """Draws the player's health as a row of heart slots, top-left.

    Placeholder rects for now (filled = health remaining, hollow outline =
    lost) — real heart art will slot into the same draw loop later, per the
    project's assets-as-files convention.
    """

    def draw(self, screen: pygame.Surface, player) -> None:
        for i in range(PLAYER_MAX_HEALTH):
            x = HUD_MARGIN + i * (HEART_SIZE + HEART_GAP)
            rect = pygame.Rect(x, HUD_MARGIN, HEART_SIZE, HEART_SIZE)
            if i < player.health:
                pygame.draw.rect(screen, COLOR_HEART, rect)
            else:
                pygame.draw.rect(screen, COLOR_HEART, rect, width=2)

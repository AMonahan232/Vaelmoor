"""Vaelmoor — entry point and main game loop."""

import pygame

from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLOR_BG
from entities.player import Player


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Vaelmoor")
        self.clock = pygame.time.Clock()
        self.running = True

        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.sprites = pygame.sprite.Group(self.player)

    def run(self) -> None:
        while self.running:
            # tick() returns milliseconds since last frame; entities take
            # seconds, so movement code can think in pixels-per-second
            dt = self.clock.tick(FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.sprites.update(dt)

            self.screen.fill(COLOR_BG)
            self.sprites.draw(self.screen)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    Game().run()

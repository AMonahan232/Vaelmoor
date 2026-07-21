"""Vaelmoor — entry point and main game loop."""

import pygame

from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLOR_BG, COLOR_SWORD, MAPS_DIR
from entities.enemy import Enemy
from entities.player import Player
from systems.tilemap import Tilemap


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Vaelmoor")
        self.clock = pygame.time.Clock()
        self.running = True

        self.tilemap = Tilemap(MAPS_DIR / "room_0.csv")
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        # A Group (not a list) so a dead enemy's kill() removes it everywhere
        self.enemies = pygame.sprite.Group(
            Enemy(x, y) for x, y in self.tilemap.enemy_spawns
        )
        self.sprites = pygame.sprite.Group(self.player, *self.enemies)

    def run(self) -> None:
        while self.running:
            # tick() returns milliseconds since last frame; entities take
            # seconds, so movement code can think in pixels-per-second
            dt = self.clock.tick(FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # KEYDOWN (not get_pressed) so holding Space can't
                # re-trigger a swing every frame
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.player.start_attack()

            self.sprites.update(dt, self.tilemap.solids)
            self.player.strike(self.enemies)

            self.screen.fill(COLOR_BG)
            self.tilemap.draw(self.screen)
            self.sprites.draw(self.screen)
            if self.player.attacking:
                pygame.draw.rect(self.screen, COLOR_SWORD, self.player.sword_hitbox)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    Game().run()

"""Vaelmoor — entry point and main game loop."""

import pygame

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    COLOR_BG,
    COLOR_SWORD,
    COLOR_TEXT,
    MAPS_DIR,
)
from entities.enemy import Enemy
from entities.player import Player
from systems.tilemap import Tilemap
from systems.hud import HUD


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Vaelmoor")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 64)
        self.hud = HUD()
        self.running = True

        # The room never changes across restarts, so load it once here rather
        # than in reset(); only the mortal things get rebuilt on death.
        self.tilemap = Tilemap(MAPS_DIR / "room_0.csv")
        self.reset()

    def reset(self) -> None:
        """(Re)build player and enemies. Shared by boot and restart so the
        two paths can't drift apart."""
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        # A Group (not a list) so a dead enemy's kill() removes it everywhere
        self.enemies = pygame.sprite.Group(
            Enemy(x, y) for x, y in self.tilemap.enemy_spawns
        )
        self.sprites = pygame.sprite.Group(self.player, *self.enemies)
        self.state = "playing"

    def run(self) -> None:
        while self.running:
            # tick() returns milliseconds since last frame; entities take
            # seconds, so movement code can think in pixels-per-second
            dt = self.clock.tick(FPS) / 1000
            self._handle_events()
            if self.state == "playing":
                self._update(dt)
            self._draw()
            pygame.display.flip()

        pygame.quit()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                # KEYDOWN (not get_pressed) so a held key can't re-trigger
                if event.key == pygame.K_SPACE and self.state == "playing":
                    self.player.start_attack()
                elif event.key == pygame.K_r and self.state == "game_over":
                    self.reset()

    def _update(self, dt: float) -> None:
        self.sprites.update(dt, self.tilemap.solids)
        self.player.strike(self.enemies)
        self._resolve_contact_damage()
        if self.player.health <= 0:
            self.state = "game_over"

    def _resolve_contact_damage(self) -> None:
        # take_hit is a no-op during i-frames, so firing it on every
        # overlapping enemy each frame is safe and stays dumb.
        for enemy in self.enemies:
            if enemy.rect.colliderect(self.player.rect):
                direction = pygame.math.Vector2(
                    self.player.rect.centerx - enemy.rect.centerx,
                    self.player.rect.centery - enemy.rect.centery,
                )
                self.player.take_hit(direction)

    def _draw(self) -> None:
        self.screen.fill(COLOR_BG)
        self.tilemap.draw(self.screen)
        self.sprites.draw(self.screen)
        if self.player.attacking:
            pygame.draw.rect(self.screen, COLOR_SWORD, self.player.sword_hitbox)
        self.hud.draw(self.screen, self.player)
        if self.state == "game_over":
            self._draw_game_over()

    def _draw_game_over(self) -> None:
        text = self.font.render("Game Over — press R", True, COLOR_TEXT)
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, rect)


if __name__ == "__main__":
    Game().run()

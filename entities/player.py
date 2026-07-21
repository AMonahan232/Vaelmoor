"""The player character."""

import pygame

from config import (
    TILE_SIZE,
    PLAYER_SPEED,
    ATTACK_DURATION,
    ATTACK_COOLDOWN,
    PLAYER_MAX_HEALTH,
    PLAYER_INVULN_TIME,
    PLAYER_KNOCK_TIME,
    KNOCKBACK_SPEED,
    BLINK_INTERVAL,
    COLOR_PLAYER,
)
from entities.entity import Entity


class Player(Entity):
    """Top-down player: 8-direction movement plus a facing-direction sword.

    A swing is just two countdown timers and a projected rect — no Sword
    sprite. The hitbox only exists while ``attack_timer`` runs, and
    ``_hit_this_swing`` ensures a multi-frame swing lands once per enemy.
    """

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, TILE_SIZE, COLOR_PLAYER)
        self.attack_timer = 0.0
        self.cooldown_timer = 0.0
        self._hit_this_swing: set = set()
        self.health = PLAYER_MAX_HEALTH
        self.invuln_timer = 0.0
        self.knock_timer = 0.0
        self.knock_dir = pygame.math.Vector2()

    @property
    def attacking(self) -> bool:
        return self.attack_timer > 0

    @property
    def invulnerable(self) -> bool:
        return self.invuln_timer > 0

    def take_hit(self, direction: pygame.math.Vector2) -> None:
        """Take contact damage — unless already in i-frames, which makes this
        a no-op. That no-op *is* the i-frame rule, so callers can safely fire
        it every overlapping frame without tracking cooldowns themselves."""
        if self.invulnerable:
            return
        self.health -= 1
        self.invuln_timer = PLAYER_INVULN_TIME
        self.knock_timer = PLAYER_KNOCK_TIME
        self.knock_dir = pygame.math.Vector2(direction)
        if self.knock_dir.length_squared() > 0:
            self.knock_dir = self.knock_dir.normalize()

    @property
    def sword_hitbox(self) -> pygame.Rect:
        """A tile-sized rect one tile from our center, along facing."""
        hitbox = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)
        offset = self.facing * TILE_SIZE
        hitbox.center = (
            self.rect.centerx + round(offset.x),
            self.rect.centery + round(offset.y),
        )
        return hitbox

    def start_attack(self) -> None:
        """Begin a swing unless still cooling down. Call on KEYDOWN, not on
        held-key state, or the sword would re-trigger every frame."""
        if self.cooldown_timer > 0:
            return
        self.attack_timer = ATTACK_DURATION
        self.cooldown_timer = ATTACK_COOLDOWN
        self._hit_this_swing.clear()

    def strike(self, enemies) -> None:
        """Land the active swing on anything the hitbox touches."""
        if not self.attacking:
            return
        hitbox = self.sword_hitbox
        for enemy in enemies:
            if enemy not in self._hit_this_swing and hitbox.colliderect(enemy.rect):
                self._hit_this_swing.add(enemy)
                enemy.take_hit(self.facing)

    def update(self, dt: float, solids: list[pygame.Rect]) -> None:
        self.attack_timer = max(0.0, self.attack_timer - dt)
        self.cooldown_timer = max(0.0, self.cooldown_timer - dt)
        self.invuln_timer = max(0.0, self.invuln_timer - dt)
        self.knock_timer = max(0.0, self.knock_timer - dt)
        self._apply_blink()

        # Knockback overrides input: being shoved back tells the player they
        # got hit, and the brief loss of control is the cost of the mistake.
        if self.knock_timer > 0:
            self._move_axis(self.knock_dir.x * KNOCKBACK_SPEED * dt, 0, solids)
            self._move_axis(0, self.knock_dir.y * KNOCKBACK_SPEED * dt, solids)
            return

        keys = pygame.key.get_pressed()
        direction = pygame.math.Vector2(
            (keys[pygame.K_RIGHT] or keys[pygame.K_d])
            - (keys[pygame.K_LEFT] or keys[pygame.K_a]),
            (keys[pygame.K_DOWN] or keys[pygame.K_s])
            - (keys[pygame.K_UP] or keys[pygame.K_w]),
        )
        if direction.length_squared() > 0:
            # Normalize so diagonal movement isn't ~41% faster than straight
            direction = direction.normalize()
            self.facing = direction

        self._move_axis(direction.x * PLAYER_SPEED * dt, 0, solids)
        self._move_axis(0, direction.y * PLAYER_SPEED * dt, solids)

    def _apply_blink(self) -> None:
        """Flicker the sprite while invulnerable; stay solid otherwise.

        The flicker itself is the visual grammar for 'temporarily safe' —
        toggling alpha on/off each BLINK_INTERVAL slice of the i-frame timer.
        """
        if not self.invulnerable:
            self.image.set_alpha(255)
            return
        slice_index = int(self.invuln_timer / BLINK_INTERVAL)
        self.image.set_alpha(60 if slice_index % 2 else 255)

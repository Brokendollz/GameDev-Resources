"""
Game Objects Module
Contains Player, Platform, Enemy, and other game entities
"""

import pygame
from .core import GameObject
from .physics import Rigidbody
from typing import List


class Player(GameObject):
    """Player character with movement and jumping."""

    def __init__(self, x: float = 100, y: float = 100, width: int = 40, height: int = 60):
        super().__init__(x, y, width, height, layer=10, color=(100, 150, 255))

        self.physics = Rigidbody(mass=1.0, gravity=800.0, friction=0.9)
        self.jump_power = 400.0  # Jump velocity
        self.move_speed = 300.0  # Horizontal movement speed
        self.max_jump_power = 500.0

        self.is_jumping = False
        self.jump_charge = 0.0
        self.direction = 1  # 1 for right, -1 for left

    def update(self, dt: float, game_objects: List[GameObject]) -> None:
        """Update player movement and physics."""
        # Get input
        keys = pygame.key.get_pressed()

        # Horizontal movement
        self.velocity_x = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.velocity_x = -self.move_speed
            self.direction = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.velocity_x = self.move_speed
            self.direction = 1

        # Jump input
        if keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
            if self.physics.on_ground and not self.is_jumping:
                self.is_jumping = True
                self.jump_charge = 0.0
        else:
            if self.is_jumping:
                # Apply jump
                if self.jump_charge > 0:
                    self.velocity_y = -self.jump_charge
                self.is_jumping = False

        # Charge jump if holding space
        if self.is_jumping and self.physics.on_ground:
            self.jump_charge += self.jump_power * 3 * dt
            self.jump_charge = min(self.jump_charge, self.max_jump_power)

        # Update physics
        platforms = [obj for obj in game_objects if isinstance(obj, Platform)]
        self.physics.update(self, dt, game_objects, platforms)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the player."""
        # Draw body
        pygame.draw.rect(surface, self.color, self.rect)

        # Draw eyes
        eye_y = self.y + 15
        left_eye_x = self.x + 10
        right_eye_x = self.x + self.width - 15

        pygame.draw.circle(surface, (255, 255, 255), (left_eye_x, eye_y), 3)
        pygame.draw.circle(surface, (255, 255, 255), (right_eye_x, eye_y), 3)

        # Draw direction indicator
        mouth_y = self.y + self.height - 10
        if self.direction > 0:
            pygame.draw.line(surface, (255, 100, 100),
                           (self.x + self.width - 10, mouth_y),
                           (self.x + self.width, mouth_y), 2)
        else:
            pygame.draw.line(surface, (255, 100, 100),
                           (self.x + 10, mouth_y),
                           (self.x, mouth_y), 2)


class Platform(GameObject):
    """Static platform that player can stand on."""

    def __init__(self, x: float, y: float, width: int, height: int = 20, color: tuple = (100, 200, 100)):
        super().__init__(x, y, width, height, layer=5, color=color)
        self.physics = None  # Platforms don't have physics

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the platform with a border."""
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)


class MovingPlatform(Platform):
    """Platform that moves back and forth."""

    def __init__(self, x: float, y: float, width: int, height: int = 20,
                 move_distance: float = 100, speed: float = 100, color: tuple = (150, 150, 200)):
        super().__init__(x, y, width, height, color)
        self.start_x = x
        self.move_distance = move_distance
        self.speed = speed
        self.direction = 1

    def update(self, dt: float, game_objects: List[GameObject]) -> None:
        """Move the platform back and forth."""
        self.x += self.speed * self.direction * dt

        # Check bounds
        if self.x < self.start_x - self.move_distance or self.x > self.start_x + self.move_distance:
            self.direction *= -1


class Enemy(GameObject):
    """Enemy that moves back and forth."""

    def __init__(self, x: float, y: float, width: int = 30, height: int = 30,
                 patrol_distance: float = 150, speed: float = 100):
        super().__init__(x, y, width, height, layer=8, color=(255, 100, 100))

        self.physics = Rigidbody(mass=1.0, gravity=800.0, friction=0.9)
        self.start_x = x
        self.patrol_distance = patrol_distance
        self.speed = speed
        self.direction = 1

        self.damage = 10

    def update(self, dt: float, game_objects: List[GameObject]) -> None:
        """Update enemy movement."""
        # Patrol movement
        self.velocity_x = self.speed * self.direction

        # Check patrol bounds
        if self.x < self.start_x - self.patrol_distance or self.x > self.start_x + self.patrol_distance:
            self.direction *= -1

        # Apply physics
        platforms = [obj for obj in game_objects if isinstance(obj, Platform)]
        self.physics.update(self, dt, game_objects, platforms)

        # Check collision with player
        player = next((obj for obj in game_objects if isinstance(obj, Player)), None)
        if player and self.check_collision(player):
            player.velocity_y = -300  # Knockback
            player.y -= 10

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the enemy."""
        pygame.draw.rect(surface, self.color, self.rect)

        # Draw angry eyes
        eye_y = self.y + 8
        left_eye_x = self.x + 8
        right_eye_x = self.x + self.width - 12

        pygame.draw.circle(surface, (255, 255, 255), (left_eye_x, eye_y), 2)
        pygame.draw.circle(surface, (255, 255, 255), (right_eye_x, eye_y), 2)

        # Draw angry eyebrows
        pygame.draw.line(surface, (255, 255, 255),
                        (left_eye_x - 3, eye_y - 2),
                        (left_eye_x + 3, eye_y - 4), 1)
        pygame.draw.line(surface, (255, 255, 255),
                        (right_eye_x - 3, eye_y - 4),
                        (right_eye_x + 3, eye_y - 2), 1)


class Collectible(GameObject):
    """Item that player can collect."""

    def __init__(self, x: float, y: float, width: int = 20, height: int = 20, value: int = 10):
        super().__init__(x, y, width, height, layer=7, color=(255, 255, 100))
        self.value = value
        self.bob_speed = 3.0
        self.bob_range = 5.0
        self.original_y = y
        self.time = 0.0

    def update(self, dt: float, game_objects: List[GameObject]) -> None:
        """Update collectible bobbing animation."""
        self.time += dt
        self.y = self.original_y + math.sin(self.time * self.bob_speed) * self.bob_range

        # Check collision with player
        player = next((obj for obj in game_objects if isinstance(obj, Player)), None)
        if player and self.check_collision(player):
            if hasattr(player, 'score'):
                player.score += self.value

            # Remove from game
            if hasattr(player, 'game_engine'):
                player.game_engine.remove_game_object(self)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the collectible as a star."""
        import math
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        radius = self.width // 2

        # Draw star
        points = []
        for i in range(10):
            angle = i * math.pi / 5 - math.pi / 2
            if i % 2 == 0:
                r = radius
            else:
                r = radius * 0.4
            x = center_x + r * math.cos(angle)
            y = center_y + r * math.sin(angle)
            points.append((x, y))

        pygame.draw.polygon(surface, self.color, points)


import math

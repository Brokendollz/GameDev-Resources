"""
Core Engine Module
Handles the main game loop and engine initialization
"""

import pygame
from pygame.locals import *
from typing import List, Optional
import sys


class GameEngine:
    """Main game engine class handling the game loop and core functionality."""

    def __init__(self, width: int = 1280, height: int = 720, fps: int = 60, title: str = "2D Platformer Engine"):
        """
        Initialize the game engine.

        Args:
            width: Window width in pixels
            height: Window height in pixels
            fps: Target frames per second
            title: Window title
        """
        pygame.init()

        self.width = width
        self.height = height
        self.fps = fps
        self.title = title

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)

        self.clock = pygame.time.Clock()
        self.running = False
        self.dt = 0  # Delta time

        self.game_objects: List[GameObject] = []
        self.background_color = (20, 20, 40)

    def add_game_object(self, obj: 'GameObject') -> None:
        """Add a game object to the engine."""
        self.game_objects.append(obj)

    def remove_game_object(self, obj: 'GameObject') -> None:
        """Remove a game object from the engine."""
        if obj in self.game_objects:
            self.game_objects.remove(obj)

    def handle_events(self) -> bool:
        """
        Handle input events.
        Returns False if quit event is received.
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
        return True

    def update(self) -> None:
        """Update all game objects."""
        for obj in self.game_objects[:]:  # Iterate over a copy
            obj.update(self.dt, self.game_objects)

    def draw(self) -> None:
        """Render all game objects."""
        self.screen.fill(self.background_color)

        # Sort objects by depth/layer
        sorted_objects = sorted(self.game_objects, key=lambda obj: obj.layer)

        for obj in sorted_objects:
            obj.draw(self.screen)

        pygame.display.flip()

    def run(self, game_loop_callback=None) -> None:
        """
        Main game loop.

        Args:
            game_loop_callback: Optional callback function called each frame
        """
        self.running = True

        while self.running:
            self.running = self.handle_events()

            if game_loop_callback:
                game_loop_callback(self)

            self.update()
            self.draw()

            self.dt = self.clock.tick(self.fps) / 1000.0  # Convert to seconds

        pygame.quit()
        sys.exit()


class GameObject:
    """Base class for all game objects."""

    def __init__(self, x: float = 0, y: float = 0, width: int = 0, height: int = 0,
                 layer: int = 0, color: tuple = (255, 255, 255)):
        """
        Initialize a game object.

        Args:
            x: X position
            y: Y position
            width: Object width
            height: Object height
            layer: Drawing layer (higher = drawn on top)
            color: RGB color tuple
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.layer = layer
        self.color = color

        self.velocity_x = 0.0
        self.velocity_y = 0.0

    @property
    def rect(self) -> pygame.Rect:
        """Get the bounding rectangle."""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, dt: float, game_objects: List['GameObject']) -> None:
        """Update the game object. Override in subclasses."""
        pass

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the game object. Override in subclasses."""
        if self.width > 0 and self.height > 0:
            pygame.draw.rect(surface, self.color, self.rect)

    def check_collision(self, other: 'GameObject') -> bool:
        """Check if this object collides with another."""
        return self.rect.colliderect(other.rect)

    def get_collisions(self, game_objects: List['GameObject']) -> List['GameObject']:
        """Get all objects this object is colliding with."""
        collisions = []
        for obj in game_objects:
            if obj is not self and self.check_collision(obj):
                collisions.append(obj)
        return collisions

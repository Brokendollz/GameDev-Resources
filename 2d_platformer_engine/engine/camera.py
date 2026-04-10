"""
Camera Module
Handles viewport and camera following
"""

import pygame
from typing import Optional


class Camera:
    """Camera system that follows the player."""

    def __init__(self, width: int, height: int, world_width: int, world_height: int):
        """
        Initialize camera.

        Args:
            width: Camera/viewport width
            height: Camera/viewport height
            world_width: Total world width
            world_height: Total world height
        """
        self.width = width
        self.height = height
        self.world_width = world_width
        self.world_height = world_height

        self.x = 0.0
        self.y = 0.0

        self.follow_target = None
        self.follow_speed = 0.15

    def set_target(self, target) -> None:
        """Set the object to follow."""
        self.follow_target = target

    def update(self, dt: float = 0) -> None:
        """Update camera position."""
        if self.follow_target is None:
            return

        # Calculate target position (center camera on target)
        target_x = self.follow_target.x - (self.width // 2) + (self.follow_target.width // 2)
        target_y = self.follow_target.y - (self.height // 2) + (self.follow_target.height // 2)

        # Smooth follow
        self.x += (target_x - self.x) * self.follow_speed
        self.y += (target_y - self.y) * self.follow_speed

        # Clamp to world bounds
        self.x = max(0, min(self.x, self.world_width - self.width))
        self.y = max(0, min(self.y, self.world_height - self.height))

    @property
    def rect(self) -> pygame.Rect:
        """Get camera rectangle."""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def to_screen_coords(self, x: float, y: float) -> tuple:
        """
        Convert world coordinates to screen coordinates.

        Args:
            x: World X coordinate
            y: World Y coordinate

        Returns:
            (screen_x, screen_y) tuple
        """
        return (x - self.x, y - self.y)

    def to_world_coords(self, x: float, y: float) -> tuple:
        """
        Convert screen coordinates to world coordinates.

        Args:
            x: Screen X coordinate
            y: Screen Y coordinate

        Returns:
            (world_x, world_y) tuple
        """
        return (x + self.x, y + self.y)

    def is_in_view(self, obj) -> bool:
        """Check if object is visible in camera view."""
        return self.rect.colliderect(obj.rect)


class Viewport:
    """Manages rendering objects within camera bounds."""

    def __init__(self, camera: Camera):
        """
        Initialize viewport.

        Args:
            camera: Camera instance to use
        """
        self.camera = camera

    def get_visible_objects(self, game_objects: list) -> list:
        """Get all objects visible in current camera view."""
        return [obj for obj in game_objects if self.camera.is_in_view(obj)]

    def draw_object(self, surface: pygame.Surface, obj) -> None:
        """Draw an object with camera offset."""
        screen_x, screen_y = self.camera.to_screen_coords(obj.x, obj.y)

        # Create temporary object with screen coordinates for drawing
        original_x = obj.x
        original_y = obj.y

        obj.x = screen_x
        obj.y = screen_y
        obj.draw(surface)

        obj.x = original_x
        obj.y = original_y

    def draw_all(self, surface: pygame.Surface, game_objects: list) -> None:
        """Draw all visible objects."""
        visible = self.get_visible_objects(game_objects)
        sorted_objects = sorted(visible, key=lambda obj: obj.layer)

        for obj in sorted_objects:
            self.draw_object(surface, obj)

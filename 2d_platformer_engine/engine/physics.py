"""
Physics Module
Handles gravity, collision resolution, and movement
"""

from typing import List, Tuple
import math


class PhysicsBody:
    """Physics component for game objects with gravity and collision."""

    def __init__(self, mass: float = 1.0, gravity: float = 800.0, friction: float = 0.95):
        """
        Initialize physics body.

        Args:
            mass: Object mass (affects gravity effect)
            gravity: Gravity acceleration in pixels/second²
            friction: Friction multiplier (0-1)
        """
        self.mass = mass
        self.gravity = gravity
        self.friction = friction

        self.on_ground = False
        self.velocity_x = 0.0
        self.velocity_y = 0.0

    def apply_gravity(self, dt: float) -> None:
        """Apply gravity to vertical velocity."""
        self.velocity_y += (self.gravity / self.mass) * dt
        self.velocity_y = min(self.velocity_y, 600)  # Terminal velocity

    def apply_friction(self) -> None:
        """Apply friction to horizontal velocity."""
        if self.on_ground:
            self.velocity_x *= self.friction

    def update_position(self, obj, dt: float) -> None:
        """
        Update object position based on velocity.

        Args:
            obj: The game object to update
            dt: Delta time in seconds
        """
        obj.x += self.velocity_x * dt
        obj.y += self.velocity_y * dt

    def check_ground_collision(self, obj, platforms: List) -> bool:
        """
        Check if object is on ground (standing on platform).

        Args:
            obj: The game object
            platforms: List of platform objects

        Returns:
            True if object is on ground
        """
        self.on_ground = False
        obj_bottom = obj.y + obj.height

        for platform in platforms:
            platform_top = platform.y
            platform_rect = platform.rect

            # Check if object is above platform and falling
            if (obj_bottom >= platform_top and
                obj_bottom <= platform_top + 10 and
                self.velocity_y >= 0):

                # Check horizontal overlap
                if obj.rect.colliderect(platform_rect):
                    obj.y = platform_top - obj.height
                    self.velocity_y = 0
                    self.on_ground = True
                    return True

        return False

    def resolve_collisions(self, obj, game_objects: List) -> None:
        """
        Resolve collisions with other objects.

        Args:
            obj: The game object
            game_objects: List of all game objects
        """
        collisions = obj.get_collisions(game_objects)

        for other in collisions:
            if hasattr(other, 'physics') and other.physics:
                # Skip if other object is also dynamic
                if hasattr(other.physics, 'is_static'):
                    continue

            self._resolve_collision(obj, other)

    def _resolve_collision(self, obj, other) -> None:
        """Handle collision between two objects."""
        # Calculate overlap
        overlap_left = (obj.x + obj.width) - other.x
        overlap_right = (other.x + other.width) - obj.x
        overlap_top = (obj.y + obj.height) - other.y
        overlap_bottom = (other.y + other.height) - obj.y

        # Find minimum overlap
        overlaps = [
            ('left', overlap_left),
            ('right', overlap_right),
            ('top', overlap_top),
            ('bottom', overlap_bottom)
        ]
        overlaps.sort(key=lambda x: x[1])

        direction = overlaps[0][0]

        if direction == 'left':
            obj.x = other.x - obj.width
            self.velocity_x = 0
        elif direction == 'right':
            obj.x = other.x + other.width
            self.velocity_x = 0
        elif direction == 'top':
            obj.y = other.y - obj.height
            self.velocity_y = 0
            self.on_ground = True
        elif direction == 'bottom':
            obj.y = other.y + other.height
            self.velocity_y = 0


class Rigidbody(PhysicsBody):
    """A dynamic physics body affected by gravity."""

    def __init__(self, mass: float = 1.0, gravity: float = 800.0, friction: float = 0.95):
        super().__init__(mass, gravity, friction)
        self.is_static = False

    def update(self, obj, dt: float, game_objects: List, platforms: List = None) -> None:
        """Update physics calculations."""
        self.velocity_x = obj.velocity_x
        self.velocity_y = obj.velocity_y

        self.apply_gravity(dt)
        self.apply_friction()

        if platforms:
            self.check_ground_collision(obj, platforms)

        self.update_position(obj, dt)
        self.resolve_collisions(obj, game_objects)

        obj.velocity_x = self.velocity_x
        obj.velocity_y = self.velocity_y


class CollisionLayer:
    """Manages collision detection between layer groups."""

    def __init__(self):
        self.static_colliders = []
        self.dynamic_colliders = []

    def add_static(self, obj) -> None:
        """Add a static (non-moving) collider."""
        self.static_colliders.append(obj)

    def add_dynamic(self, obj) -> None:
        """Add a dynamic (moving) collider."""
        self.dynamic_colliders.append(obj)

    def check_collisions(self) -> List[Tuple]:
        """
        Check all collisions.

        Returns:
            List of (obj1, obj2) collision pairs
        """
        collisions = []

        for dynamic in self.dynamic_colliders:
            for static in self.static_colliders:
                if dynamic.check_collision(static):
                    collisions.append((dynamic, static))

        return collisions

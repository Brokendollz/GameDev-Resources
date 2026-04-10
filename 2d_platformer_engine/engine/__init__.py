"""
2D Platformer Engine
A complete game engine for creating 2D platformer games
"""

from .core import GameEngine, GameObject
from .physics import PhysicsBody, Rigidbody, CollisionLayer
from .objects import Player, Platform, MovingPlatform, Enemy, Collectible
from .camera import Camera, Viewport
from .level import Level, LevelBuilder, LevelManager, create_demo_level

__version__ = "1.0.0"

__all__ = [
    "GameEngine",
    "GameObject",
    "PhysicsBody",
    "Rigidbody",
    "CollisionLayer",
    "Player",
    "Platform",
    "MovingPlatform",
    "Enemy",
    "Collectible",
    "Camera",
    "Viewport",
    "Level",
    "LevelBuilder",
    "LevelManager",
    "create_demo_level",
]

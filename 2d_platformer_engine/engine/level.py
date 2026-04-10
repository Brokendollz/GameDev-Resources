"""
Level Module
Handles level design and management
"""

from .objects import Player, Platform, MovingPlatform, Enemy, Collectible
from .core import GameObject
from typing import List, Dict, Tuple


class Level:
    """Represents a game level with platforms and enemies."""

    def __init__(self, width: int = 2400, height: int = 1200):
        """
        Initialize a level.

        Args:
            width: Level width in pixels
            height: Level height in pixels
        """
        self.width = width
        self.height = height
        self.objects: List[GameObject] = []

    def add_object(self, obj: GameObject) -> None:
        """Add an object to the level."""
        self.objects.append(obj)

    def add_platform(self, x: float, y: float, width: int, height: int = 20,
                     color: tuple = (100, 200, 100)) -> Platform:
        """Create and add a static platform."""
        platform = Platform(x, y, width, height, color)
        self.add_object(platform)
        return platform

    def add_moving_platform(self, x: float, y: float, width: int, height: int = 20,
                           move_distance: float = 100, speed: float = 100,
                           color: tuple = (150, 150, 200)) -> MovingPlatform:
        """Create and add a moving platform."""
        platform = MovingPlatform(x, y, width, height, move_distance, speed, color)
        self.add_object(platform)
        return platform

    def add_enemy(self, x: float, y: float, patrol_distance: float = 150,
                  speed: float = 100) -> Enemy:
        """Create and add an enemy."""
        enemy = Enemy(x, y, patrol_distance=patrol_distance, speed=speed)
        self.add_object(enemy)
        return enemy

    def add_collectible(self, x: float, y: float, value: int = 10) -> Collectible:
        """Create and add a collectible item."""
        item = Collectible(x, y, value=value)
        self.add_object(item)
        return item

    def create_spawn_point(self, x: float = 100, y: float = 100) -> Player:
        """Create and add the player spawn point."""
        player = Player(x, y)
        self.add_object(player)
        return player

    def get_all_objects(self) -> List[GameObject]:
        """Get all objects in the level."""
        return self.objects


class LevelBuilder:
    """Builder pattern for creating levels."""

    def __init__(self, width: int = 2400, height: int = 1200):
        """Initialize level builder."""
        self.level = Level(width, height)

    def add_platform(self, x: float, y: float, width: int, height: int = 20) -> 'LevelBuilder':
        """Add a static platform."""
        self.level.add_platform(x, y, width, height)
        return self

    def add_moving_platform(self, x: float, y: float, width: int, move_distance: float = 100,
                           speed: float = 100) -> 'LevelBuilder':
        """Add a moving platform."""
        self.level.add_moving_platform(x, y, width, move_distance=move_distance, speed=speed)
        return self

    def add_enemy(self, x: float, y: float, patrol_distance: float = 150,
                  speed: float = 100) -> 'LevelBuilder':
        """Add an enemy."""
        self.level.add_enemy(x, y, patrol_distance, speed)
        return self

    def add_collectible(self, x: float, y: float, value: int = 10) -> 'LevelBuilder':
        """Add a collectible."""
        self.level.add_collectible(x, y, value)
        return self

    def spawn_player(self, x: float = 100, y: float = 100) -> 'LevelBuilder':
        """Add player spawn point."""
        self.level.create_spawn_point(x, y)
        return self

    def build(self) -> Level:
        """Build and return the level."""
        return self.level


class LevelManager:
    """Manages multiple levels and level progression."""

    def __init__(self):
        """Initialize level manager."""
        self.levels: Dict[str, Level] = {}
        self.current_level = None
        self.current_level_name = None

    def add_level(self, name: str, level: Level) -> None:
        """Add a level to the manager."""
        self.levels[name] = level

    def load_level(self, name: str) -> Level:
        """Load a level by name."""
        if name not in self.levels:
            raise ValueError(f"Level '{name}' not found")

        self.current_level = self.levels[name]
        self.current_level_name = name
        return self.current_level

    def get_current_level(self) -> Level:
        """Get the currently loaded level."""
        return self.current_level

    def next_level(self) -> bool:
        """Move to next level. Returns True if successful."""
        if self.current_level_name is None:
            return False

        level_names = list(self.levels.keys())
        current_index = level_names.index(self.current_level_name)

        if current_index + 1 < len(level_names):
            next_name = level_names[current_index + 1]
            self.load_level(next_name)
            return True

        return False

    def get_level_names(self) -> List[str]:
        """Get all available level names."""
        return list(self.levels.keys())


def create_demo_level() -> Level:
    """Create a demo level for testing."""
    builder = LevelBuilder(width=2400, height=1200)

    # Ground platforms
    builder.add_platform(0, 1100, 2400, 100)  # Main ground

    # Starting area
    builder.spawn_player(100, 1000)

    # Tutorial platforms
    builder.add_platform(200, 950, 150)
    builder.add_platform(450, 900, 150)
    builder.add_platform(700, 850, 150)

    # Moving platform section
    builder.add_moving_platform(1000, 800, 150, move_distance=200, speed=150)
    builder.add_moving_platform(1300, 700, 150, move_distance=150, speed=120)

    # Enemy section
    builder.add_platform(1600, 900, 300)
    builder.add_enemy(1700, 850, patrol_distance=200, speed=120)
    builder.add_enemy(1850, 850, patrol_distance=200, speed=120)

    # Collectibles
    builder.add_collectible(250, 920, 10)
    builder.add_collectible(500, 870, 10)
    builder.add_collectible(750, 820, 10)
    builder.add_collectible(1100, 770, 15)
    builder.add_collectible(1400, 670, 15)
    builder.add_collectible(1750, 820, 20)

    # Jump challenge
    builder.add_platform(2000, 950, 80)
    builder.add_platform(2100, 900, 80)
    builder.add_platform(2200, 850, 80)
    builder.add_collectible(2150, 820, 25)

    return builder.build()

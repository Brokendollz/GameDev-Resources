# 2D Platformer Engine

A complete, production-ready 2D platformer game engine built with Python and Pygame. This engine provides all the essential components needed to create 2D platformer games.

## Features

- **Game Engine**: Core game loop and rendering system
- **Physics System**: Gravity, collision detection, and resolution
- **Game Objects**: Player, platforms, moving platforms, enemies, and collectibles
- **Camera System**: Smooth camera following with viewport culling
- **Level Management**: Easy level creation and switching
- **Input Handling**: Keyboard-based player control
- **Collision Detection**: Rectangle-based collision with physics response

## Installation

### Requirements

- Python 3.7+
- Pygame

### Setup

```bash
pip install pygame
```

## Quick Start

### Running the Demo

```bash
python examples/demo_game.py
```

### Creating Your First Game

```python
from engine import GameEngine, LevelBuilder, Camera, Viewport, Player

# Create engine
engine = GameEngine(width=1280, height=720, title="My Game")

# Build level
builder = LevelBuilder()
builder.spawn_player(100, 100)
builder.add_platform(0, 500, 1000, 50)
builder.add_platform(300, 400, 200)
builder.add_enemy(400, 300, patrol_distance=150)
builder.add_collectible(350, 250, value=10)

level = builder.build()

# Load objects into engine
for obj in level.get_all_objects():
    engine.add_game_object(obj)

# Setup camera
player = next(obj for obj in engine.game_objects if isinstance(obj, Player))
camera = Camera(1280, 720, 2400, 1200)
camera.set_target(player)
viewport = Viewport(camera)

# Run game
engine.run()
```

## Architecture

### Core Components

#### GameEngine
The main engine class that handles:
- Window management
- Game loop
- Object management
- Rendering

#### GameObject
Base class for all game objects with:
- Position and dimensions
- Velocity
- Layer (z-order)
- Collision detection

#### Physics System

**Rigidbody**: Physics component for dynamic objects
- Gravity simulation
- Velocity and acceleration
- Collision response
- Ground detection

### Game Objects

**Player**: Controllable character
- Movement (A/D or Arrow Keys)
- Jumping (Space/W/Up Arrow)
- Physics-based movement
- Collision handling

**Platform**: Static platform
- Basic rectangle collision
- Visual rendering

**MovingPlatform**: Platform that moves back and forth
- Configurable movement range and speed
- Useful for puzzle elements

**Enemy**: Patrolling enemy
- Autonomous movement
- Collision damage
- Knockback on player collision

**Collectible**: Item to collect
- Bobbing animation
- Score value
- Auto-collection on contact

### Camera System

**Camera**: Follows a target object
- Smooth interpolation
- World boundary clamping
- Coordinate conversion (world ↔ screen)

**Viewport**: Manages visible objects
- Frustum culling
- Viewport-relative rendering

### Level System

**Level**: Container for all game objects

**LevelBuilder**: Fluent API for level creation
```python
builder = LevelBuilder(width=2400, height=1200)
builder.spawn_player(100, 100) \
       .add_platform(0, 500, 1000) \
       .add_moving_platform(1000, 400, 200) \
       .add_enemy(500, 300) \
       .add_collectible(300, 250)
```

**LevelManager**: Manages multiple levels
- Load levels by name
- Level progression
- Level switching

## Controls

| Input | Action |
|-------|--------|
| A / Left Arrow | Move Left |
| D / Right Arrow | Move Right |
| Space / W / Up Arrow | Jump (hold for higher jump) |
| R | Reset Level |
| Escape | Quit |

## Customization

### Creating Custom Objects

```python
from engine import GameObject
from engine.physics import Rigidbody

class PowerUp(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 30, 30, layer=7, color=(255, 200, 0))
        self.rotation = 0
    
    def update(self, dt, game_objects):
        self.rotation += dt * 360
    
    def draw(self, surface):
        # Draw custom shape
        pygame.draw.circle(surface, self.color, 
                         (int(self.x + self.width/2), 
                          int(self.y + self.height/2)), 
                         15)
```

### Modifying Physics

```python
# Player physics adjustment
player = Player(100, 100)
player.physics.gravity = 1200  # Higher gravity
player.physics.friction = 0.85  # More friction
player.jump_power = 500  # Higher jump
player.move_speed = 400  # Faster movement
```

### Custom Game Loop

```python
def my_game_loop(engine):
    # Custom logic here
    camera.update()
    engine.screen.fill((0, 0, 0))
    viewport.draw_all(engine.screen, engine.game_objects)
    # Draw custom UI, particles, etc.

engine.run(my_game_loop)
```

## Performance Tips

1. **Use Viewport Culling**: Only visible objects are processed
2. **Layer Organization**: Objects are sorted by layer once per frame
3. **Object Pooling**: Reuse collectibles for frequent items
4. **Physics Optimization**: Only enable physics for objects that need it

## Examples

### Example 1: Demo Game (`examples/demo_game.py`)
Full-featured game with UI, scoring, and multiple challenges.

### Example 2: Custom Level (`examples/custom_level.py`)
Shows how to create a custom level using the LevelBuilder.

## API Reference

### GameEngine

```python
engine = GameEngine(width=1280, height=720, fps=60, title="Game")
engine.add_game_object(obj)
engine.remove_game_object(obj)
engine.run(callback=None)
```

### LevelBuilder

```python
builder = LevelBuilder(width=2400, height=1200)
builder.spawn_player(x, y)
builder.add_platform(x, y, width, height=20)
builder.add_moving_platform(x, y, width, move_distance=100, speed=100)
builder.add_enemy(x, y, patrol_distance=150, speed=100)
builder.add_collectible(x, y, value=10)
level = builder.build()
```

### Camera

```python
camera = Camera(viewport_width, viewport_height, world_width, world_height)
camera.set_target(target_object)
camera.update()
screen_coords = camera.to_screen_coords(world_x, world_y)
world_coords = camera.to_world_coords(screen_x, screen_y)
```

## Contributing

Contributions are welcome! Please ensure:
- Code follows PEP 8 style guide
- New features include documentation
- Examples demonstrate new functionality

## License

MIT License - See LICENSE file for details

## Future Enhancements

- [ ] Audio system (sound effects and music)
- [ ] Particle effects system
- [ ] Advanced collision shapes (circles, polygons)
- [ ] Level editor GUI
- [ ] Mobile/touch input support
- [ ] Animation system
- [ ] Tile-based level support
- [ ] Multiplayer networking
- [ ] Save/load system

## Troubleshooting

**Game runs slowly**: Check object count with `len(engine.game_objects)`. Consider using viewport culling.

**Physics feels wrong**: Adjust `gravity`, `friction`, and `jump_power` values.

**Collision issues**: Ensure objects have proper width/height and check collision layer setup.

## Support

For issues and questions, please open an issue on the repository.

---

**Version**: 1.0.0  
**Last Updated**: 2026-04-10

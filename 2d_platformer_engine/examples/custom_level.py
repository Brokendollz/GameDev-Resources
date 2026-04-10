"""
Custom Level Example
Demonstrates how to create a custom level using the engine
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine import GameEngine, Camera, Viewport, LevelBuilder
import pygame


def create_custom_level():
    """Create a custom level with specific design."""
    builder = LevelBuilder(width=3000, height=1500)

    # Ground
    builder.add_platform(0, 1400, 3000, 100)

    # Spawn player
    builder.spawn_player(50, 1300)

    # Section 1: Basic platforming
    builder.add_platform(200, 1300, 150, 20, )
    builder.add_platform(450, 1200, 150)
    builder.add_platform(700, 1100, 150)
    builder.add_platform(950, 1000, 150)

    # Section 2: Moving platforms challenge
    for i in range(5):
        x = 1200 + i * 250
        y = 900 - i * 100
        builder.add_moving_platform(x, y, 120, move_distance=100, speed=80)

    # Section 3: Enemy gauntlet
    builder.add_platform(2300, 1200, 400)
    for i in range(3):
        builder.add_enemy(2350 + i * 100, 1150, patrol_distance=150, speed=100)

    # Section 4: Collectible maze
    builder.add_platform(2900, 1000, 100)
    builder.add_collectible(2950, 970, 50)

    # Add some vertical challenge
    for i in range(8):
        builder.add_platform(500 + i * 150, 700 - i * 60, 100)

    return builder.build()


def main():
    """Run the custom level."""
    # Create engine
    engine = GameEngine(width=1280, height=720, title="Custom Level Example")

    # Create and load level
    level = create_custom_level()
    for obj in level.get_all_objects():
        engine.add_game_object(obj)

    # Setup camera
    player = next((obj for obj in engine.game_objects
                   if hasattr(obj, 'is_jumping')), None)  # Find player
    camera = Camera(1280, 720, level.width, level.height)
    if player:
        camera.set_target(player)

    viewport = Viewport(camera)

    def game_loop(engine_instance):
        """Custom game loop."""
        camera.update()
        engine_instance.screen.fill((30, 30, 60))
        viewport.draw_all(engine_instance.screen, engine_instance.game_objects)

        # Draw simple HUD
        font = pygame.font.Font(None, 24)
        if player:
            score = getattr(player, 'score', 0)
            fps = engine_instance.clock.get_fps()
            hud_text = font.render(f"Score: {score} | FPS: {int(fps)}", True, (255, 255, 255))
            engine_instance.screen.blit(hud_text, (10, 10))

    engine.run(game_loop)


if __name__ == "__main__":
    main()

"""
Demo Game
A simple platformer game using the 2D Platformer Engine
"""

import sys
import os
import pygame

# Add parent directory to path for importing engine
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine import (
    GameEngine, Player, Platform, Camera, Viewport,
    LevelManager, create_demo_level
)


class DemoGame:
    """Main demo game class."""

    def __init__(self):
        """Initialize the demo game."""
        self.engine = GameEngine(width=1280, height=720, title="2D Platformer - Demo")

        # Create level manager
        self.level_manager = LevelManager()
        demo_level = create_demo_level()
        self.level_manager.add_level("demo", demo_level)
        self.level_manager.load_level("demo")

        # Load level objects
        level = self.level_manager.get_current_level()
        for obj in level.get_all_objects():
            self.engine.add_game_object(obj)

        # Get player reference
        self.player = next((obj for obj in self.engine.game_objects if isinstance(obj, Player)), None)
        if self.player:
            self.player.score = 0
            self.player.game_engine = self.engine

        # Camera setup
        self.camera = Camera(1280, 720, level.width, level.height)
        if self.player:
            self.camera.set_target(self.player)

        self.viewport = Viewport(self.camera)

        # UI setup
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)

        # Game state
        self.game_over = False
        self.game_over_time = 0

    def handle_game_input(self, dt: float) -> None:
        """Handle game-specific input."""
        keys = pygame.key.get_pressed()

        # Reset level on R
        if keys[pygame.K_r]:
            self.__init__()

    def update(self, dt: float) -> None:
        """Update game logic."""
        # Update camera
        self.camera.update()

        # Check if player fell off the world
        if self.player and self.player.y > 2000:
            self.game_over = True
            self.game_over_time = 0

        # Game over state
        if self.game_over:
            self.game_over_time += dt
            if self.game_over_time > 2.0:
                self.__init__()  # Restart

    def draw_ui(self) -> None:
        """Draw UI elements."""
        # Draw score
        if self.player:
            score_text = self.font.render(f"Score: {self.player.score}", True, (255, 255, 255))
            self.engine.screen.blit(score_text, (10, 10))

        # Draw controls
        controls = [
            "A/D or Arrows - Move",
            "Space/W/Up - Jump",
            "R - Reset Level",
        ]

        for i, control in enumerate(controls):
            control_text = self.font.render(control, True, (200, 200, 200))
            self.engine.screen.blit(control_text, (10, 60 + i * 35))

        # Draw game over screen
        if self.game_over:
            # Semi-transparent overlay
            overlay = pygame.Surface((1280, 720))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.engine.screen.blit(overlay, (0, 0))

            # Game over text
            game_over_text = self.large_font.render("GAME OVER", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(640, 300))
            self.engine.screen.blit(game_over_text, text_rect)

            # Final score
            final_score = self.font.render(f"Final Score: {self.player.score}", True, (255, 255, 255))
            score_rect = final_score.get_rect(center=(640, 400))
            self.engine.screen.blit(final_score, score_rect)

            # Restart instruction
            restart_text = self.font.render("Press R to Restart", True, (200, 200, 200))
            restart_rect = restart_text.get_rect(center=(640, 500))
            self.engine.screen.blit(restart_text, restart_rect)

    def game_loop_callback(self, engine: GameEngine) -> None:
        """Callback for each game loop iteration."""
        self.handle_game_input(engine.dt)
        self.update(engine.dt)

        # Clear and draw with camera
        engine.screen.fill(engine.background_color)

        # Draw level objects
        self.viewport.draw_all(engine.screen, engine.game_objects)

        # Draw UI
        self.draw_ui()

        pygame.display.flip()

    def run(self) -> None:
        """Run the demo game."""
        self.engine.run(self.game_loop_callback)


def main():
    """Entry point."""
    game = DemoGame()
    game.run()


if __name__ == "__main__":
    main()

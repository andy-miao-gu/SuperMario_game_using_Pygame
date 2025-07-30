import pygame

class GameState:
    def __init__(self):
        self.state = "playing"  # "playing", "game_over", "menu"
        self.font = None
        self.big_font = None
        
    def initialize_fonts(self):
        """
        Initialize fonts for UI
        """
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
    def draw_game_over_screen(self, screen, score, level):
        """
        Draw the game over screen
        """
        if not self.font:
            self.initialize_fonts()
            
        # Semi-transparent overlay
        overlay = pygame.Surface((1200, 800))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = self.big_font.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(600, 300))
        screen.blit(game_over_text, game_over_rect)
        
        # Score text
        score_text = self.font.render(f"Final Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(600, 380))
        screen.blit(score_text, score_rect)
        
        # Level text
        level_text = self.font.render(f"Level Reached: {level}", True, (255, 255, 255))
        level_rect = level_text.get_rect(center=(600, 420))
        screen.blit(level_text, level_rect)
        
        # Instructions
        restart_text = self.font.render("Press R to Restart or ESC to Quit", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(600, 500))
        screen.blit(restart_text, restart_rect)
        
    def draw_hud(self, screen, score, level, enemies_defeated, time_survived):
        """
        Draw the heads-up display during gameplay
        """
        if not self.font:
            self.initialize_fonts()
            
        # Score
        score_text = self.font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        # Level
        level_text = self.font.render(f"Level: {level}", True, (255, 255, 255))
        screen.blit(level_text, (10, 50))
        
        # Enemies defeated
        enemies_text = self.font.render(f"Enemies Avoided: {enemies_defeated}", True, (255, 255, 255))
        screen.blit(enemies_text, (10, 90))
        
        # Time survived
        time_seconds = time_survived // 60
        time_text = self.font.render(f"Time: {time_seconds}s", True, (255, 255, 255))
        screen.blit(time_text, (10, 130))
        
        # Instructions
        help_text = pygame.font.Font(None, 24).render("Use Arrow Keys to Move and Jump High, Avoid the Colored Enemies at All Heights!", True, (255, 255, 255))
        screen.blit(help_text, (10, 760))

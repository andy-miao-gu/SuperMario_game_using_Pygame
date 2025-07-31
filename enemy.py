import pygame
import random
from config import START_Y

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type="basic"):
        super().__init__()
        self.enemy_type = enemy_type
        self.speed = random.randint(2, 5)  # Random speed for variety
        self.original_y = y  # Store original Y position for floating enemies
        self.float_timer = 0  # For floating animation
        
        # Create larger enemies that span more screen width
        if enemy_type == "basic":
            self.image = pygame.Surface((120, 40))  # Much wider
            self.image.fill((255, 0, 0))  # Red enemy
            # Add a border to make it more visible
            pygame.draw.rect(self.image, (128, 0, 0), self.image.get_rect(), 2)
        elif enemy_type == "fast":
            self.image = pygame.Surface((100, 30))  # Wider
            self.image.fill((255, 165, 0))  # Orange enemy
            pygame.draw.rect(self.image, (200, 100, 0), self.image.get_rect(), 2)
            self.speed += 3
        elif enemy_type == "big":
            self.image = pygame.Surface((150, 60))  # Much wider and taller
            self.image.fill((128, 0, 128))  # Purple enemy
            pygame.draw.rect(self.image, (64, 0, 64), self.image.get_rect(), 3)
            self.speed -= 1
        elif enemy_type == "wall":
            self.image = pygame.Surface((200, 50))  # Very wide wall-like enemy
            self.image.fill((255, 0, 255))  # Magenta enemy
            pygame.draw.rect(self.image, (128, 0, 128), self.image.get_rect(), 4)
            self.speed -= 2
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self, camera_offset=0):
        """
        Move enemy from right to left with floating animation for aerial enemies
        """
        self.rect.x -= self.speed
        
        # Add floating motion for enemies that are not on the ground
        if self.rect.y < START_Y - 50:  # If enemy is above ground level
            self.float_timer += 0.1
            import math
            float_offset = int(10 * math.sin(self.float_timer))
            self.rect.y = self.original_y + float_offset
        
    def is_off_screen(self):
        """
        Check if enemy has moved off the left side of screen
        """
        return self.rect.x < -100

class EnemyManager:
    def __init__(self):
        self.enemies = pygame.sprite.Group()
        self.spawn_timer = 0
        self.spawn_delay = 15  # Very fast spawning - every 0.25 seconds at 60 FPS
        self.level = 1
        self.enemies_defeated = 0
        self.time_survived = 0
        
    def update(self):
        """
        Update all enemies and spawn new ones
        """
        self.time_survived += 1
        
        # Update all enemies
        for enemy in self.enemies:
            enemy.update()
            
        # Remove enemies that are off screen
        for enemy in self.enemies:
            if enemy.is_off_screen():
                self.enemies.remove(enemy)
                self.enemies_defeated += 1
                
        # Spawn new enemies - MASSIVE SPAWNING!
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay:
            # Spawn MULTIPLE enemies every time!
            num_enemies = random.randint(3, 8)  # Spawn 3-8 enemies at once
            for i in range(num_enemies):
                new_enemy = self.create_enemy_at_random_position()
                new_enemy.rect.x += i * 50  # Offset each enemy
                self.enemies.add(new_enemy)
            
            # Also spawn some enemies with random spacing
            if random.random() < 0.7:  # 70% chance for extra wave
                for i in range(random.randint(2, 5)):
                    extra_enemy = self.create_enemy_at_random_position()
                    extra_enemy.rect.x += random.randint(150, 400)  # Random spacing
                    self.enemies.add(extra_enemy)
            
            self.spawn_timer = 0
            
        # Increase difficulty over time - MUCH MORE FREQUENT
        if self.time_survived > 0 and self.time_survived % 180 == 0:  # Every 3 seconds!
            self.level_up()
            
    def spawn_enemy(self):
        """
        Spawn a new enemy from the right side at random heights
        """
        new_enemy = self.create_enemy_at_random_position()
        self.enemies.add(new_enemy)
        
    def create_enemy_at_random_position(self):
        """
        Create an enemy at a random position
        """
        # Random enemy type based on level
        enemy_types = ["basic"]
        if self.level >= 2:
            enemy_types.append("fast")
        if self.level >= 3:
            enemy_types.append("big")
        if self.level >= 5:
            enemy_types.append("wall")  # Very challenging wall enemy
            
        enemy_type = random.choice(enemy_types)
        
        # Spawn at right side of screen
        x = 1300  # Off screen to the right
        
        # Get enemy height based on type
        if enemy_type == "basic":
            enemy_height = 40  # Height unchanged
        elif enemy_type == "fast":
            enemy_height = 30  # Height unchanged
        elif enemy_type == "big":
            enemy_height = 60  # Height unchanged
        elif enemy_type == "wall":
            enemy_height = 50  # Wall enemy height
        
        # Random Y positions - only lower side of screen where Mario can reach
        possible_y_positions = [
            START_Y - enemy_height,      # Ground level (where Mario walks)
            START_Y - enemy_height,      # Ground level (increased chance)
            START_Y - enemy_height,      # Ground level (more chance)
            START_Y - enemy_height,      # Ground level (even more chance)
            START_Y - enemy_height - 50, # Slightly above ground
            START_Y - enemy_height - 50, # Slightly above ground (more chance)
            START_Y - enemy_height - 100, # Low platform
            START_Y - enemy_height - 100, # Low platform (more chance)
            START_Y - enemy_height - 150, # Medium-low platform
            START_Y - enemy_height - 150, # Medium-low platform (more chance)
            START_Y - enemy_height - 200, # Medium platform
            START_Y - enemy_height - 200, # Medium platform (more chance)
            START_Y - enemy_height - 250, # Medium-high platform
            START_Y - enemy_height - 300, # High platform (Mario's max jump reach)
            600, # Lower area
            650, # Lower-mid area
            700, # Lower area
            750, # Near bottom of screen
        ]
        
        # Choose random Y position
        y = random.choice(possible_y_positions)
        
        return Enemy(x, y, enemy_type)
        
    def level_up(self):
        """
        Increase difficulty - MUCH MORE AGGRESSIVE
        """
        self.level += 1
        if self.spawn_delay > 5:  # Much faster minimum spawn rate
            self.spawn_delay -= 2  # Reduce spawn delay more aggressively
            
    def draw(self, screen):
        """
        Draw all enemies
        """
        self.enemies.draw(screen)
        
    def check_collision(self, mario_rect):
        """
        Check if Mario collides with any enemy
        """
        for enemy in self.enemies:
            if mario_rect.colliderect(enemy.rect):
                return True
        return False
        
    def get_score(self):
        """
        Return current score based on time survived and enemies defeated
        """
        time_bonus = self.time_survived // 60  # 1 point per second
        enemy_bonus = self.enemies_defeated * 10
        level_bonus = (self.level - 1) * 50
        return time_bonus + enemy_bonus + level_bonus

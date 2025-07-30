import pygame
from mario import Mario
from enemy import EnemyManager
from game_state import GameState
from config import START_X, START_Y
a = 0
b=0
def main():
    # Initialize pygame
    pygame.init()
    

    # Set up the screen dimensions and create the window
    screen = pygame.display.set_mode((1200, 800))
    bg = pygame.image.load('Assets/images/bg.png')
    bg = pygame.transform.scale(bg, (1200, 800))
    pygame.display.set_caption("Mario Game")

    # Create the Mario instance
    mario = Mario()
    
    # Create enemy manager and game state
    enemy_manager = EnemyManager()
    game_state = GameState()

    # Set up clock for controlling the frame rate
    clock = pygame.time.Clock()

    # Background scrolling variables
    camera_x = 0  # Camera offset for horizontal scrolling
    scroll_margin_left = 400  # Distance from left edge before scrolling starts
    scroll_margin_right = 800  # Distance from right edge before scrolling starts

    # Game loop
    running = True
    image_index = 0
    check = True
    while running:
        clock.tick(60)  # Limit frame rate to 60 FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_state.state == "game_over":
                    if event.key == pygame.K_r:
                        # Restart game
                        mario = Mario()
                        enemy_manager = EnemyManager()
                        game_state.state = "playing"
                        camera_x = 0
                        image_index = 0
                    elif event.key == pygame.K_ESCAPE:
                        running = False

        if game_state.state == "playing":
            keys = pygame.key.get_pressed()

            # Reset moving state
            mario.is_moving = False

            # Check for keypresses
            if keys[pygame.K_LEFT]:
                mario.is_moving = True
                mario.face_direction = 'left'  # Set face direction for jump images
                image_index -= 0.2
                # Check if Mario should scroll the camera or move normally
                if mario.rect.x > scroll_margin_left:
                    mario.rect.x -= 3
                else:
                    # Scroll the background instead
                    camera_x += 3


            elif keys[pygame.K_RIGHT]:
                mario.is_moving = True
                mario.face_direction = 'right'  # Set face direction for jump images
                image_index += 0.2
                # Check if Mario should scroll the camera or move normally
                if mario.rect.x < scroll_margin_right:
                    mario.rect.x += 3
                else:
                    # Scroll the background instead
                    camera_x -= 3
            else:
                # Continue animation for standing even when not moving (faster for waving)
                image_index += 0.25


            if keys[pygame.K_UP] and not mario.is_jumping:
                mario.is_jumping = True
                mario.velocity_y = mario.jump_speed
                
            # Update enemy manager
            enemy_manager.update()
            
            # Check for collision with enemies
            if enemy_manager.check_collision(mario.rect):
                game_state.state = "game_over"
            

        # Fill the screen with black before drawing
        camera_x %= 1200
        # Draw background with camera offset for scrolling effect
        screen.blit(bg, (camera_x, 0))
        # Draw a second background image to create seamless scrolling
        screen.blit(bg, (camera_x + 1200, 0))
        screen.blit(bg, (camera_x - 1200, 0))
        
        # Draw invisible platforms for visual reference (optional) - only lower side
        platform_color = (100, 100, 100, 100)  # Semi-transparent gray
        platform_positions = [550, 500, 450, 400, 350, 300, 600, 650, 700, 750]
        for platform_y in platform_positions:
            # Draw subtle platform lines across the screen
            pygame.draw.line(screen, (80, 80, 80), (0, platform_y), (1200, platform_y), 1)

        if game_state.state == "playing":
            # Update Mario
            a = mario.rect.y
            mario.update(image_index)
            b = mario.rect.y
            if a > b:
                mario.jump_index = 0
            else:
                mario.jump_index = 1
                
            # Draw Mario
            mario.draw(screen)
            
            # Draw enemies
            enemy_manager.draw(screen)
            
            # Draw HUD
            game_state.draw_hud(screen, enemy_manager.get_score(), enemy_manager.level, 
                              enemy_manager.enemies_defeated, enemy_manager.time_survived)
            
        elif game_state.state == "game_over":
            # Still draw Mario and enemies in background
            mario.draw(screen)
            enemy_manager.draw(screen)
            
            # Draw game over screen
            game_state.draw_game_over_screen(screen, enemy_manager.get_score(), enemy_manager.level)

        # Update display
        pygame.display.update()

    # Quit pygame
    pygame.quit()

if __name__ == "__main__":
    main()

import pygame
from mario import Mario
from config import START_X, START_Y
a = 0
b=0
def main():
    # Initialize pygame
    pygame.init()
    

    # Set up the screen dimensions and create the window
    screen = pygame.display.set_mode((1200, 800))
    bg = pygame.image.load('Assets/images/bg.png')
    pygame.display.set_caption("Mario Game")

    # Create the Mario instance
    mario = Mario()

    # Set up clock for controlling the frame rate
    clock = pygame.time.Clock()

    # Game loop
    running = True
    image_index = 0
    face_direction = 'left'  # 1 for right, -1 for left
    check = True
    while running:
        clock.tick(60)  # Limit frame rate to 60 FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Check for keypresses
        if keys[pygame.K_LEFT]:
            image_index -= 0.2
            mario.rect.x -= 3
            if mario.is_jumping and face_direction == 'left':  # Flip the jump images only while jumping
                # Flip the entire jump images list
                mario.jumpimages = [pygame.transform.flip(img, True, False) for img in mario.jumpimages]
                mario.image = mario.jumpimages[0]  # Update image during jump
            face_direction = 'right'


        elif keys[pygame.K_RIGHT]:
            image_index += 0.2
            mario.rect.x += 3
            if mario.is_jumping and face_direction == 'right':  # If jumping, ensure not to flip the jump images
                mario.jumpimages = [pygame.transform.flip(img, True, False) for img in mario.jumpimages]
                mario.image = mario.jumpimages[1]
            face_direction = 'left'
            


        if keys[pygame.K_UP] and not mario.is_jumping:
            mario.is_jumping = True
            mario.velocity_y = mario.jump_speed
            

        # Fill the screen with black before drawing
        screen.blit(bg,(0,0))

        a = mario.rect.y
        mario.update(image_index)
        b = mario.rect.y
        if a > b:
            mario.jump_index = 0
        else:
            mario.jump_index = 1
        mario.draw(screen)

        # Update display
        pygame.display.update()

    # Quit pygame
    pygame.quit()

if __name__ == "__main__":
    main()

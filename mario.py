import pygame

class Mario(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.specimages = []
        self.load_images()
        self.current_image_index = 0
        self.image = self.specimages[self.current_image_index]
        self.rect = self.image.get_rect()

    def load_images(self):
        # Load images from the folder and store them in a list
        for i in range(1, 14):  # Assuming you have 12 Stickman images
            img = pygame.image.load(f'Assets/images/Stickman/Stickman {i}.png')
            img = pygame.transform.scale(img, (50, 100))  # Adjust size
            self.specimages.append(img)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, image_index):
        # Update the image index based on the key presses (left or right)
        self.current_image_index = image_index % len(self.specimages)
        self.image = self.specimages[self.current_image_index]

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    mario = Mario()
    running = True
    image_index = 0  # Variable to hold the image index
    mario.load_images()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()  # Get state of all keys
        if keys[pygame.K_LEFT]:
            image_index += 0.154 # Increment index when left key is pressed
            mario.rect.x -= 1.23  # Move left
        if keys[pygame.K_RIGHT]:
            image_index -= 0.154  # Decrement index when right key is pressed
            mario.rect.x += 1.23  # Move left

        
        screen.fill((0,0,0))
        mario.update(int(image_index))
        mario.draw(screen)
        pygame.display.update()
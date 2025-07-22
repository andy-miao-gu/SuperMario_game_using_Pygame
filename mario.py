import pygame

class Mario(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.specimages = []
        self.jumpimages = []
        self.load_images()
        self.current_image_index = 0
        self.image = self.specimages[self.current_image_index]
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 600  # ground level

        self.is_jumping = False
        self.jump_speed = -10
        self.gravity = 0.5
        self.velocity_y = 0
        self.jump_index = 0

    def load_images(self):
        for i in range(1, 14):
            img = pygame.image.load(f'Assets/images/Stickman/Stickman walk/Stickman {i}.png')
            img = pygame.transform.scale(img, (50, 100))
            self.specimages.append(img)
        for i in range(1, 4):
            img = pygame.image.load(f'Assets/images/Stickman/Jump/Jump {i}.png')
            img = pygame.transform.scale(img, (50, 100))
            self.jumpimages.append(img)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, image_index):
        if self.is_jumping:
            # Show jump image
            self.jump_index = int((self.jump_index + 0.2) % len(self.jumpimages))
            self.image = self.jumpimages[int(self.jump_index)]
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y

            if self.rect.y >= 600:
                self.rect.y = 600
                self.is_jumping = False
                self.velocity_y = 0
        else:
            # Walking animation
            self.current_image_index = image_index % len(self.specimages)
            self.image = self.specimages[self.current_image_index]

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    mario = Mario()
    clock = pygame.time.Clock()

    running = True
    image_index = 0

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            image_index += 0.2
            mario.rect.x -= 3
        if keys[pygame.K_RIGHT]:
            image_index += 0.2
            mario.rect.x += 3
        if keys[pygame.K_UP] and not mario.is_jumping:
            mario.is_jumping = True
            mario.velocity_y = mario.jump_speed

        screen.fill((0, 0, 0))
        mario.update(int(image_index))
        mario.draw(screen)
        pygame.display.update()

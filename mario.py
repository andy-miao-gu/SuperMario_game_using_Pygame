import pygame
from config import START_X, START_Y, JUMP_SPEED, GRAVITY
from assets import AssetLoader

class Mario(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.specimages = []  # Images for walking
        self.jumpimages = []  # Images for jumping
        self.load_images()
        self.current_image_index = 0
        self.image = self.specimages[self.current_image_index]
        self.rect = self.image.get_rect()
        self.rect.x = START_X
        self.rect.y = START_Y

        self.is_jumping = False
        self.jump_speed = JUMP_SPEED
        self.gravity = GRAVITY
        self.velocity_y = 0
        self.jump_index = 0

    def load_images(self):
        """
        Loads walking and jumping images.
        """
        self.specimages = AssetLoader.load_walk_images()
        self.jumpimages = AssetLoader.load_jump_images()

    def draw(self, screen):
        """
        Draw Mario on the screen.
        """
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, image_index):
        """
        Updates Mario's movement and animation.
        """
        if self.is_jumping:
            # Jumping animation=
            self.image = self.jumpimages[int(self.jump_index)]
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y

            if self.rect.y >= START_Y:
                self.rect.y = START_Y
                self.is_jumping = False
                self.velocity_y = 0
        else:
            # Walking animation
            self.current_image_index = int(image_index) % len(self.specimages)
            self.image = self.specimages[self.current_image_index]

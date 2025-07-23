import pygame
from config import WALK_IMAGES_PATH, JUMP_IMAGES_PATH, NUM_WALK_IMAGES, NUM_JUMP_IMAGES

class AssetLoader:
    @staticmethod
    def load_images(path, count, size=(50, 100)):
        """
        Load and return a list of images from a given path.
        """
        images = []
        for i in range(1, count + 1):
            img = pygame.image.load(f'{path}{i}.png')
            img = pygame.transform.scale(img, size)
            images.append(img)
        return images

    @staticmethod
    def load_walk_images():
        return AssetLoader.load_images(WALK_IMAGES_PATH, NUM_WALK_IMAGES)

    @staticmethod
    def load_jump_images():
        return AssetLoader.load_images(JUMP_IMAGES_PATH, NUM_JUMP_IMAGES)

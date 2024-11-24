# platform.py

import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image=None):
        super().__init__()
        if image:
            self.image = pygame.transform.scale(image, (width, height))
        else:
            self.image = pygame.Surface((width, height))
            self.image.fill((255, 255, 255))  # Default color
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
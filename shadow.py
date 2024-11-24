# shadow.py

import pygame

class Shadow(pygame.sprite.Sprite):
    def __init__(self, image, platforms):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.midbottom = (200, 410)
        self.pos = pygame.math.Vector2(self.rect.midbottom)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0.5)
        self.platforms = platforms

    def move(self):
        self.acc = pygame.math.Vector2(0, 0.5)  # Gravity
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # Boundary conditions
        if self.pos.x < self.rect.width / 2:
            self.pos.x = self.rect.width / 2
            self.vel.x = 0
        if self.pos.x > 400 - self.rect.width / 2:
            self.pos.x = 400 - self.rect.width / 2
            self.vel.x = 0

        self.rect.midbottom = self.pos

    def update(self):
        self.move()
        hits = pygame.sprite.spritecollide(self, self.platforms, False)
        if hits:
            self.pos.y = hits[0].rect.top + 1
            self.vel.y = 0
            self.rect.midbottom = self.pos

    def reset_position(self):
        self.pos = pygame.math.Vector2(200, 410)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0.5)
        self.rect.midbottom = self.pos
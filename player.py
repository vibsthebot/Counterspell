# player.py

import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, image, platforms):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.midbottom = (10, 410)
        self.pos = pygame.math.Vector2(self.rect.midbottom)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.platforms = platforms
        self.jump_count = 0
        self.MAX_JUMPS = 2

    def move(self):
        self.acc = pygame.math.Vector2(0, 0.5)  # Gravity

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_a]:
            self.acc.x = -0.5
        if pressed_keys[pygame.K_d]:
            self.acc.x = 0.5

        if pressed_keys[pygame.K_SPACE]:
            self.jump()

        # Apply friction
        self.acc.x += self.vel.x * -0.12
        # Equations of motion
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

    def jump(self):
        if self.jump_count < self.MAX_JUMPS:
            self.jump_count += 1
            self.vel.y = -10

    def update(self):
        self.move()
        hits = pygame.sprite.spritecollide(self, self.platforms, False)
        if hits:
            self.pos.y = hits[0].rect.top + 1
            self.vel.y = 0
            self.jump_count = 0
            self.rect.midbottom = self.pos

    def reset_position(self):
        self.pos = pygame.math.Vector2(10, 410)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.rect.midbottom = self.pos
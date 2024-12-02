import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((234, 208, 168))  # Platform color (Beige)
        self.rect = pygame.Rect(x, y, width, height)


    def draw(self, surface):
        pygame.draw.rect(surface, (234, 208, 168), self.rect)
    def move(self):
        pass 

class MovingPlatform(Platform):
    def __init__(self, x, y, width, height, boundary_top, boundary_bottom, speed):
        super().__init__(x, y, width, height)
        self.boundary_top = boundary_top
        self.boundary_bottom = boundary_bottom
        self.speed = speed
        self.direction = -1  # -1 for up, 1 for down

    def update(self):
        self.rect.y += self.speed * self.direction
        if self.rect.top <= self.boundary_top or self.rect.bottom >= self.boundary_bottom:
            self.direction *= -1  # Reverse direction
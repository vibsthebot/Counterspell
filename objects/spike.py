import pygame

pygame.init()

displaysurface = pygame.display.set_mode((0, 0))
pygame.display.set_caption("Mirror Wars")

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, original):
        super().__init__()
        try:
            self.image = pygame.transform.scale(pygame.image.load("images/spike.png").convert_alpha(), (20, 20))  # Adjust size as needed
        except pygame.error as e:
            print(f"Unable to load spike image: {e}")
            
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x-40, y)
        self.pos = pygame.math.Vector2(self.rect.midbottom)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.original = original

    def update(self):
        # If spikes are stationary, no need to update position
        pass
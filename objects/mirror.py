import pygame

pygame.init()

displaysurface = pygame.display.set_mode((0, 0))
pygame.display.set_caption("Mirror Wars")

class Mirror(pygame.sprite.Sprite):
    finished_current_level = False
    def __init__(self, x, y, M1, P1):
        super().__init__()
        try:
            self.image = pygame.transform.scale(pygame.image.load("images/mirror.png").convert_alpha(), (40, 40))  # Adjust size as needed
        except pygame.error as e:
            print(f"Unable to load mirror image: {e}")
            
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x-40, y)
        self.pos = pygame.math.Vector2(self.rect.midbottom)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.M1 = M1
        self.P1 = P1

    def update(self):
        if pygame.sprite.collide_rect(self, self.P1):
            #print("Collided with mirror")
            if self.M1.isDead:
                # Handle the case when M1 is dead, e.g., restart the level or end the game
                self.M1.finished_current_level = True
                #print("M1 is dead")
    def draw(self, surface):
        pass
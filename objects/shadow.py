import pygame

vec = pygame.math.Vector2
pygame.init()

# Constants
HEIGHT = 450
WIDTH = 400
GRAVITY = 0.5
ACC = 0.5
FRIC = -0.12
FPS = 60

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mirror Wars")

shadowPic = pygame.transform.scale(pygame.image.load("images/shadowspriteFINAL.png").convert_alpha(), (40, 70))
shadowRunning = pygame.transform.scale(pygame.image.load("images/shadowrunning.png").convert_alpha(), (40, 70))

class Shadow(pygame.sprite.Sprite):
    def __init__(self, x, y, platforms):
        super().__init__()
        try:
            self.image = shadowPic
        except pygame.error as e:
            print(f"Unable to load player image: {e}")
            
        self.rect = self.image.get_rect()
        #print(self.rect)
        self.pos = vec((x, y))
        self.vel = vec(0, 0)
        self.acc = vec(0, GRAVITY)
        self.jump_count = 0
        self.MAX_JUMPS = 1  # Allow double jumps
        self.mirrored_move = False
        self.isDead = False
        self.finished_current_level = False
        self.platforms = platforms

    def move(self):
        self.acc = vec(0, GRAVITY)  # Apply gravity

        pressed_keys = pygame.key.get_pressed()
        if self.mirrored_move:
            if pressed_keys[pygame.K_a] and pressed_keys[pygame.K_d]:
                self.acc.x = 0
                self.image = shadowPic
            elif pressed_keys[pygame.K_d]:
                self.acc.x = -ACC
                self.image = pygame.transform.flip(shadowRunning, True, False)
            elif pressed_keys[pygame.K_a]:
                self.acc.x = ACC
                self.image = shadowRunning
            else:
                self.image = shadowPic
        else:
            if pressed_keys[pygame.K_a] and pressed_keys[pygame.K_d]:
                self.acc.x = 0
                self.image = shadowPic
            elif pressed_keys[pygame.K_a]:
                self.acc.x = -ACC
                self.image = pygame.transform.flip(shadowRunning, True, False)
            elif pressed_keys[pygame.K_d]:
                self.acc.x = ACC
                self.image = shadowRunning
            else:
                self.image = shadowPic

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # Prevent moving beyond the left and right edges
        if self.pos.x < self.rect.width / 2:
            self.pos.x = self.rect.width / 2
            self.vel.x = 0
        if self.pos.x > WIDTH - self.rect.width / 2:
            self.pos.x = WIDTH - self.rect.width / 2
            self.vel.x = 0

        self.rect.midbottom = self.pos
        #print(self.rect.midbottom)

    def jump(self):
        if self.jump_count < self.MAX_JUMPS:
            self.jump_count += 1
            self.vel.y = -11

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)  # Line thickness 2

    def update(self):
        self.move()
        rect = self.rect
        for collide in self.rect_collide():
            collide = collide.rect
            #print(collide)
            if self.rect.centery < collide.bottom or self.rect.midtop[1] > collide.top:
                if self.rect.centery < collide.bottom:
                    self.pos.y = collide.top + 1
                    self.vel.y = 0
                    self.jump_count = 0
                elif self.rect.midtop[1] > collide.top:
                    self.pos.y = collide.bottom + self.rect.height + 1
                    self.vel.y = 0.1
                #print('a')
            if collide.clipline((rect.topleft[0], rect.topleft[1]+5), (rect.bottomleft[0], rect.bottomleft[1] - 5)) or collide.clipline((rect.topright[0], rect.topright[1]+5), (rect.bottomright[0], rect.bottomright[1] - 5)):
                if collide.clipline((rect.topleft[0], rect.topleft[1]+5), (rect.bottomleft[0], rect.bottomleft[1] - 5)):
                    if collide.clipline((rect.topright[0], rect.topright[1]+5), (rect.bottomright[0], rect.bottomright[1] - 5)):
                        print()
                    else:
                        self.pos.x = collide.right + self.rect.width / 2
                        self.vel.x = 0
                elif collide.clipline((rect.topright[0], rect.topright[1]+5), (rect.bottomright[0], rect.bottomright[1] - 5)):
                    if collide.clipline((rect.topleft[0], rect.topleft[1]+5), (rect.bottomleft[0], rect.bottomleft[1] - 5)):
                        print()
                    else:
                        self.pos.x = collide.left - self.rect.width / 2
                        self.vel.x = 0
            self.rect.midbottom = self.pos

    def rect_collide(self):
        list_of_platforms = [] 
        for platform in self.platforms:
            if self.rect.colliderect(platform.rect):
                list_of_platforms.append(platform)
        return list_of_platforms

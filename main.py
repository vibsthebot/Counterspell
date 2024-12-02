import asyncio
import random
from time import sleep
import pygame
from pygame.locals import *
from objects.player import Player
from objects.shadow import Shadow
from objects.platforms import Platform, MovingPlatform
from objects.spike import Spike
from objects.mirror import Mirror
#from level_creator import level_creator

# Initialize Pygame
pygame.init()

# Define vectors for position, velocity, acceleration
vec = pygame.math.Vector2

# Constants
HEIGHT = 450
WIDTH = 400
GRAVITY = 0.5
ACC = 0.5
FRIC = -0.12
FPS = 60

FramePerSec = pygame.time.Clock()

# Set up the display
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mirror Wars")

# Define game states
PLAYING = 1
GAME_OVER = 0

# Initialize game state
game_state = PLAYING

# Define sprite groups
all_sprites = pygame.sprite.Group()
global platforms, moving_platforms, spikes, player, shadow, mirror
platforms = pygame.sprite.Group()
moving_platforms = pygame.sprite.Group()
spikes = pygame.sprite.Group()

def level_creator(platform_data, mirror_coords, player_coords, shadow_coords):
    global all_sprites, platforms, spikes, moving_platforms, player, shadow, mirror

    # Clear existing sprites
    platforms.empty()
    spikes.empty()
    moving_platforms.empty()
    all_sprites.empty()

    # Create player and shadow
    player = Player(player_coords[0], player_coords[1], platforms)
    shadow = Shadow(shadow_coords[0], shadow_coords[1], platforms)

    # Create mirror
    mirror = Mirror(mirror_coords[0], mirror_coords[1], shadow, player)

    # Add platforms and obstacles
    for item in platform_data:
        if item['type'] == 'platform':
            platform = Platform(*item['coords'])
            platforms.add(platform)
            all_sprites.add(platform)
        elif item['type'] == 'moving_platform':
            platform = MovingPlatform(*item['coords'], *item['movement'])
            platforms.add(platform)
            moving_platforms.add(platform)
            all_sprites.add(platform)
        elif item['type'] == 'spike':
            spike = Spike(*item['coords'], True)
            spikes.add(spike)
            all_sprites.add(spike)
    floor = Platform(0, HEIGHT - 20, WIDTH, 20)
    top = Platform(0, -20, WIDTH, 20)

    # Add player and shadow to all_sprites
    all_sprites.add(player, shadow, mirror)
    platforms.add(floor, top)
    all_sprites.add(floor, top)

# Define the kill_screen function with Restart button
def kill_screen(displaysurface):
    global game_state, level  # To modify the global game state variable

    # Define fonts
    game_over_font = pygame.font.Font(None, 74)
    button_font = pygame.font.Font(None, 50)

    # Render "Game Over" text
    game_over_text = game_over_font.render('Game Over', True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 50))

    # Define "Restart" button
    restart_text = button_font.render('Restart', True, (255, 255, 255))
    restart_button = pygame.Rect(0, 0, 200, 50)
    restart_button.center = (WIDTH / 2, HEIGHT / 2 + 50)
    
    # Button colors
    button_color = (0, 255, 0)
    button_hover_color = (0, 200, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_pos):
                    levels[level - 1]()
                    
                    game_state = PLAYING
                    return

        # Fill the screen with black
        displaysurface.fill((0, 0, 0))

        # Draw "Game Over" text
        displaysurface.blit(game_over_text, game_over_rect)

        # Check if mouse is over the restart button
        mouse_pos = pygame.mouse.get_pos()
        if restart_button.collidepoint(mouse_pos):
            current_button_color = button_hover_color
        else:
            current_button_color = button_color

        # Draw "Restart" button
        pygame.draw.rect(displaysurface, current_button_color, restart_button)
        displaysurface.blit(restart_text, restart_text.get_rect(center=restart_button.center))

        # Update the display
        pygame.display.flip()
        FramePerSec.tick(FPS)

# Initialize or reset the game
# Convert existing levels to the new format

def level1():
    platform_data = [
        {'type': 'platform', 'coords': (0, 320, 50, 20)},
    ]
    mirror_coords = (200, 430)
    player_coords = (10, 410)
    shadow_coords = (10, 200)
    level_creator(platform_data, mirror_coords, player_coords, shadow_coords)

def level2():
    platform_data = [
        {'type': 'platform', 'coords': (0, 430, 50, 20)},
        {'type': 'platform', 'coords': (80, 320, 80, 10)},
        {'type': 'platform', 'coords': (160, 220, 80, 10)},
        {'type': 'platform', 'coords': (240, 160, 80, 10)},
        {'type': 'platform', 'coords': (320, 80, 80, 10)},
    ]
    mirror_coords = (300, 39)
    player_coords = (104, 410)
    shadow_coords = (104, 70)
    level_creator(platform_data, mirror_coords, player_coords, shadow_coords)

def level3():
    platform_data = [
        {'type': 'platform', 'coords': (203, 236, 80, 10)},
        {'type': 'platform', 'coords': (29, 327, 80, 10)},
        {'type': 'platform', 'coords': (48, 103, 80, 10)},
        {'type': 'platform', 'coords': (292, 150, 80, 10)},
        {'type': 'platform', 'coords': (39, 240, 80, 10)},
        {'type': 'platform', 'coords': (254, 340, 80, 10)},
    ]
    mirror_coords = (317, 39)
    player_coords = (104, 410)
    shadow_coords = (104, 70)
    level_creator(platform_data, mirror_coords, player_coords, shadow_coords)

def level4():
    platform_data = [
        {'type': 'platform', 'coords': (50, 300, 100, 10)},   # HEIGHT - 150 = 300
        {'type': 'platform', 'coords': (250, 230, 100, 10)},  # HEIGHT - 220 = 230
        # Add more platforms as desired
    ]
    mirror_coords = (WIDTH / 2, 190)  # HEIGHT - 260 = 190
    player_coords = (50, 370)         # HEIGHT - 80 = 370
    shadow_coords = (350, 370)
    level_creator(platform_data, mirror_coords, player_coords, shadow_coords)

def level5():
    platform_data = [
        {'type': 'platform', 'coords': (100, 270, 200, 20)},  # HEIGHT - 180 = 270
        {'type': 'platform', 'coords': (50, 150, 100, 20)},   # HEIGHT - 300 = 150
        {'type': 'platform', 'coords': (250, 150, 100, 20)},  # HEIGHT - 300 = 150
        # Add more platforms as desired
    ]
    mirror_coords = (WIDTH / 2, 110)  # HEIGHT - 340 = 110
    player_coords = (50, 370)         # HEIGHT - 80 = 370
    shadow_coords = (350, 370)
    level_creator(platform_data, mirror_coords, player_coords, shadow_coords)

def level1():
    platform_data = [
        {'type': 'platform', 'coords': (0, HEIGHT - 40, WIDTH, 40)},  # Ground
        {'type': 'platform', 'coords': (50, HEIGHT - 100, 100, 10)},
        {'type': 'spike', 'coords': (200, HEIGHT - 50)},
    ]
    mirror_coords = (WIDTH / 2, HEIGHT - 150)
    player_coords = (50, HEIGHT - 80)
    shadow_coords = (350, HEIGHT - 80)
    level_creator(platform_data, mirror_coords, player_coords, shadow_coords)

def level2():
    platform_data = [
        {'type': 'platform', 'coords': (0, HEIGHT - 40, WIDTH, 40)},
        {'type': 'moving_platform', 'coords': (100, HEIGHT - 200, 100, 10), 'movement': (HEIGHT - 300, HEIGHT - 100, 2)},
        {'type': 'platform', 'coords': (250, HEIGHT - 250, 100, 10)},
        {'type': 'spike', 'coords': (150, HEIGHT - 50)},
        {'type': 'spike', 'coords': (300, HEIGHT - 50)},
    ]
    mirror_coords = (WIDTH / 2, HEIGHT - 300)
    player_coords = (50, HEIGHT - 80)
    shadow_coords = (350, HEIGHT - 80)
    level_creator(platform_data, mirror_coords, player_coords, shadow_coords)

def level3():
    platform_data = [
        {'type': 'platform', 'coords': (0, HEIGHT - 40, WIDTH, 40)},
        {'type': 'platform', 'coords': (50, HEIGHT - 150, 100, 10)},
        {'type': 'platform', 'coords': (250, HEIGHT - 150, 100, 10)},
        {'type': 'moving_platform', 'coords': (150, HEIGHT - 250, 100, 10), 'movement': (70, HEIGHT - 150, 3)},
        {'type': 'spike', 'coords': (WIDTH / 2, HEIGHT - 50)},
    ]
    mirror_coords = (WIDTH / 2, HEIGHT - 400)
    player_coords = (50, HEIGHT - 80)
    shadow_coords = (350, HEIGHT - 80)
    level_creator(platform_data, mirror_coords, player_coords, shadow_coords)

def level4():
    platform_data = [
        {'type': 'platform', 'coords': (0, HEIGHT - 40, WIDTH, 40)},
        {'type': 'platform', 'coords': (0, HEIGHT - 100, 80, 10)},
        {'type': 'platform', 'coords': (320, HEIGHT - 100, 80, 10)},
        {'type': 'moving_platform', 'coords': (160, HEIGHT - 150, 80, 10), 'movement': (HEIGHT - 250, HEIGHT - 90, 2)},
        {'type': 'spike', 'coords': (80, HEIGHT - 50)},
        {'type': 'spike', 'coords': (240, HEIGHT - 50)},
    ]
    mirror_coords = (WIDTH / 2, HEIGHT - 300)
    player_coords = (50, HEIGHT - 80)
    shadow_coords = (350, HEIGHT - 80)
    level_creator(platform_data, mirror_coords, player_coords, shadow_coords)

def level5():
    platform_data = [
        {'type': 'platform', 'coords': (0, HEIGHT - 40, WIDTH, 40)},
        {'type': 'moving_platform', 'coords': (100, HEIGHT - 100, 200, 10), 'movement': (HEIGHT - 300, HEIGHT - 50, 4)},
        {'type': 'spike', 'coords': (WIDTH / 2 - 50, HEIGHT - 50)},
        {'type': 'spike', 'coords': (WIDTH / 2 + 50, HEIGHT - 50)},
    ]
    mirror_coords = (WIDTH / 2, HEIGHT - 350)
    player_coords = (50, HEIGHT - 80)
    shadow_coords = (350, HEIGHT - 80)
    level_creator(platform_data, mirror_coords, player_coords, shadow_coords)


levels = [level1, level2, level3, level4, level5]
def run_level():
    global game_state, player, shadow
    PLAYING = 1
    GAME_OVER = 0
    game_state = PLAYING
    print("Running level")
    while shadow.finished_current_level == False:
        if game_state == PLAYING:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    ()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        player.jump()
                        shadow.jump()
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                    elif event.key == pygame.K_s and player.spike_not_placed:
                        # Place a spike at the player's current position
                        spike = Spike(player.rect.centerx, player.rect.bottom, False)
                        all_sprites.add(spike)
                        spikes.add(spike)
                        player.spike_not_placed = False
                    elif event.key == pygame.K_f and pygame.sprite.collide_rect(player, mirror):
                        if shadow.mirrored_move:
                            shadow.mirrored_move = False
                        else:
                            shadow.mirrored_move = True

            # Update and move sprites
            #player.move()
            #shadow.move()
            all_sprites.update()
            #all_sprites.draw(displaysurface)
            #pygame.display.flip()

            # Check for collisions between spikes and other sprites (e.g., Shadow)
            collisions = pygame.sprite.groupcollide(spikes, all_sprites, False, False)
            for spike, hit_sprites in collisions.items():
                for sprite in hit_sprites:
                    if sprite != player and isinstance(sprite, Shadow):
                        if spike.original == False:
                            shadow.isDead = True
                            sprite.kill()   # Remove the Shadow
                            spike.kill()    # Optionally remove the spike after collision
                    elif sprite == player:
                        
                        print("Player hit by spike")
                        game_state = GAME_OVER
                        kill_screen(displaysurface)

            if pygame.sprite.collide_rect(player, shadow) and shadow.isDead == False:
                print("Player hit by shadow")
                game_state = GAME_OVER
                kill_screen(displaysurface)

            # Render everything
            background = pygame.transform.scale(pygame.image.load('images/background.png'), (400, 450))
            displaysurface.blit(background, (0, 0))  # Draw the background image
            all_sprites.draw(displaysurface)
            player.draw(displaysurface)
            shadow.draw(displaysurface)
            pygame.display.flip()
            #sleep(10)
            FramePerSec.tick(FPS)
            #sleep(1)

        elif game_state == GAME_OVER:
            kill_screen(displaysurface)

def win_screen():
    font = pygame.font.Font(None, 74)
    text = font.render('You Win!', True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))

    while True:
        '''for event in pygame.event.get():
            if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                game_loop()
                return'''

        displaysurface.fill((0, 0, 0))
        displaysurface.blit(text, text_rect)
        pygame.display.flip()
        FramePerSec.tick(FPS)

def intro_page():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False

        displaysurface.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render('Mirror Wars', True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 50))
        displaysurface.blit(text, text_rect)

        font_small = pygame.font.Font(None, 36)
        instructions = font_small.render('Press space to start', True, (255, 255, 255))
        instructions_rect = instructions.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))
        displaysurface.blit(instructions, instructions_rect)

        pygame.display.flip()
        FramePerSec.tick(FPS)

def about_page():
    about = True
    while about:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                about = False

        displaysurface.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render('About', True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 150))
        displaysurface.blit(text, text_rect)

        font_small = pygame.font.Font(None, 36)
        about_lines = [
    'You feel a split within your',
    'soul. An evil shadow', 
    'materializes before you.',  'Rid the world of',  'this corruption.',
    'Cleanse your soul.'
]

        y_offset = 100  # Updated starting y position
        for line in about_lines:
            line_surface = font_small.render(line, True, (255, 255, 255))
            displaysurface.blit(line_surface, (50, y_offset))
            y_offset += 30  # Adjust line height as needed

        continue_text = font_small.render('Press space to continue', True, (255, 255, 255))
        continue_rect = continue_text.get_rect(center=(WIDTH / 2, HEIGHT - 50))  # Move it near the bottom
        displaysurface.blit(continue_text, continue_rect)

        pygame.display.flip()
        FramePerSec.tick(FPS)

def controls_page():
    controls = True
    while controls:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                controls = False

        displaysurface.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render('Controls', True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 50))
        displaysurface.blit(text, text_rect)

        font_small = pygame.font.Font(None, 36)
        # Render control instructions separately
        controls_text1 = font_small.render('Use A/D to move, W to jump.', True, (255, 255, 255))
        controls_text2 = font_small.render('F reverses your shadow when', True, (255, 255, 255))
        controls_text3 = font_small.render('you are in contact with a mirror,', True, (255, 255, 255))
        controls_text4 = font_small.render('and G sets it back to normal.', True, (255, 255, 255))

        # Set starting positions
        x_position = 25  # Adjust as needed
        y_position = 200  # Starting y position for controls

        # Blit the control texts to the display surface
        displaysurface.blit(controls_text1, (x_position, y_position))
        displaysurface.blit(controls_text2, (x_position, y_position + 30))
        displaysurface.blit(controls_text3, (x_position, y_position + 60))
        displaysurface.blit(controls_text4, (x_position, y_position + 90))

        # Render "Press space to continue" lower on the screen
        continue_text = font_small.render('Press space to continue', True, (255, 255, 255))
        continue_rect = continue_text.get_rect(center=(WIDTH / 2, HEIGHT - 50))
        displaysurface.blit(continue_text, continue_rect)

        pygame.display.flip()
        FramePerSec.tick(FPS)

def game_loop():
    global level
    for i in levels:
        level = levels.index(i) + 1
        i()  # Call the level function
        run_level()
    '''level1()
    run_level()
    level2()
    run_level()
    level3()
    run_level()'''
    win_screen()

async def main():
    intro_page()
    about_page()
    controls_page()
    game_loop()
    await asyncio.sleep(0)

asyncio.run(main())
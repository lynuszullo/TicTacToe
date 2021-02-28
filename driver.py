# Simple pygame program

# Import and initialize the pygame library
import pygame

import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

# Set up the drawing window
# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_RED = 0
SCREEN_GREEN = 0
SCREEN_BLUE = 0
FONT_COLOR = (255, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Title
pygame.display.set_caption("Asteroid Dodger 2021!")

# Load images
start_img = pygame.image.load('img/start_btn.png')
exit_img = pygame.image.load('img/exit_btn.png')

# Main menu screen
main_menu = True

# Score
myfont = pygame.font.SysFont("monospace", 16)


# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        # self.surf =
        self.surf = pygame.transform.scale(pygame.image.load("rocket.png").convert(), (20, 20))
        self.surf = pygame.transform.rotate(self.surf, -90)
        self.surf.set_colorkey((247, 247, 247), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.transform.scale(pygame.image.load("asteroid.png").convert(), (20, 20))

        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(1, 5)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        screen.blit(self.image, self.rect)

        return action


# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

# Instantiate player. Right now, this is just a rectangle.
player = Player()

# Groups are good to enable you to modify classes of sprtites with methods
# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# set score to 0
score = 0

# Start and exit buttons
start_button = Button(SCREEN_WIDTH // 2 - 350, SCREEN_HEIGHT // 2, start_img)
exit_button = Button(SCREEN_WIDTH // 2 + 150, SCREEN_HEIGHT // 2, exit_img)

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Run until the user asks to quit
running = True
while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

            # Add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    # We are in the main menu
    if main_menu:
        if start_button.draw():
            main_menu = False
        if exit_button.draw():
            running = False

    else:

        # Draw background
        screen.fill((SCREEN_RED, SCREEN_GREEN, SCREEN_BLUE))

        # Gets keys and updates player
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        enemies.update()

        # Draw the player on the screen
        # screen.blit(player.surf, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        # screen.blit(player.surf, player.rect)


        # Draw all sprites
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Check if any enemies have collided with the player
        if pygame.sprite.spritecollideany(player, enemies):
            # If so, then remove the player and stop the loop
            player.kill()
            running = False

        # Updates score

        scoretext = myfont.render("Score {0}".format(score), True, (FONT_COLOR))
        screen.blit(scoretext, (5, 10))
        score += 1

        pygame.display.flip()

        # Ensure program maintains a rate of 30 frames per second
        clock.tick(30)

        # Draw a solid blue circle in the center
        # pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

        # Update the display
    pygame.display.update()

# Done! Time to quit.
pygame.quit()

import pygame
import os
from time import sleep
import asyncio 
import threading



WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FPS = 60
HEIGHT, WIDTH = 900, 900
SHIP_SIZE = (50, 50)
red_bullet = 100
yellow_bullet = 100000
YELLOW_LIVES = 10
RED_LIVES = 10
YELLOW = (255,255,0)
DIFFCULTY_LEVEL = 100 # speed at which yellow ship can shoot at!

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
red_rect = pygame.Rect(10, 200, 40, 40)

# Background image
background = pygame.image.load(os.path.join("Assets/space_background.png"))
background_scaled = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Yellow ship, LEFT ONE
yellow = pygame.image.load(os.path.join("Assets/spaceship_yellow.png"))
yellow = pygame.transform.rotate(yellow, -90)
yellow_ship = pygame.transform.scale(yellow, SHIP_SIZE)

# Red ship, RIGHT ONE
red = pygame.image.load(os.path.join("Assets/spaceship_red.png"))
red = pygame.transform.rotate(red, 90)
red_ship = pygame.transform.scale(red, SHIP_SIZE)

# Bullet display count
font = pygame.font.Font(None, 40)
red_bullet_count = font.render(F"{red_bullet}", True, WHITE)
yellow_bullet_count = font.render(f"{yellow_bullet}", True, WHITE)
font_yellow_lives = font.render(f"LIVES {YELLOW_LIVES}",True,WHITE)
font_red_lives = font.render(f"LIVES {RED_LIVES}",True,WHITE)


def yellow_ship_shoot(location_red_ship, location_yellow_ship):
    if location_red_ship[1] == location_yellow_ship[1]:
        bullet = pygame.Surface((5, 5))
        bullet.fill(YELLOW)
        return bullet
    else:
        return None

def shoot_bullet(events):
    bullet = None
    for event in events:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullet = pygame.Surface((5, 5))
            bullet.fill(RED)
    return bullet

def move_bullets(bullets_fired):
    for bullet in bullets_fired:
        bullet[1][0] += 10

def yellow_bullets_move(yellow_bullets_fired):
    for bullet in yellow_bullets_fired:
        bullet[1][0] -= 10

def move_ship(ship_location):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        ship_location[1] = max(ship_location[1] - 10, 0)
    elif keys[pygame.K_DOWN]:
        ship_location[1] = min(ship_location[1] + 10, HEIGHT - SHIP_SIZE[1])

def draw_screen(divider_block, background_scaled,
                red_bullet_count, yellow_bullet_count, 
                ship_location, bullets_fired,
                font_yellow_lives, font_red_lives,
                RED_LOCATION, yellow_bullets_fired):
    screen.blit(background_scaled, (0, 0))
    screen.blit(yellow_ship, (ship_location[0], ship_location[1]))  # position
    screen.blit(red_bullet_count, (10, 20))  # position
    screen.blit(yellow_bullet_count, (WIDTH//2 + 20, 20))  # position
    screen.blit(red_ship, RED_LOCATION)  # position
    screen.blit(font_yellow_lives, (200, 20))  # position
    screen.blit(font_red_lives, (700, 20))  # position

    for bullet in yellow_bullets_fired:
        screen.blit(bullet[0], (bullet[1][0], bullet[1][1]))  # SURFACE OBJECT, (POSITION)

    for bullet in bullets_fired:  # RED BULLETS
        screen.blit(bullet[0], (bullet[1][0], bullet[1][1]))
    
    screen.blit(divider_block, (WIDTH // 2 + 10, 0))  # position
    pygame.display.flip()

def yellow_ship_movement(location_red_ship, location_yellow_ship):
    # MOVE THE YELLOW SHIP TO THE POSITION OF THE RED SHIP
    if location_red_ship[1] < location_yellow_ship[1]:
        location_red_ship[1] += 5
    elif location_red_ship[1] > location_yellow_ship[1]:
        location_red_ship[1] -= 5

def main():
    global red_bullet, yellow_bullet, red_bullet_count, yellow_bullet_count, RED_LIVES, YELLOW_LIVES
    global font_red_lives, font_yellow_lives, DIFFCULTY_LEVEL
    ship_location = [0, 450]  # YELLOW SHIP IS THE ONE ON THE LEFT
    RED_LOCATION = [850, 450]  # RED SHIP IS THE ONE ON THE RIGHT
    clock = pygame.time.Clock()
    bullets_fired = []  # [bullet object,[x,y],...] # bullets fired by the red ship
    yellow_bullets_fired = []  # bullets fired by the yellow ship
    last_yellow_shot_time = 0  # Initialize last shot time for the yellow ship
    # Divide the screen in half
    divider_block = pygame.Surface((5, HEIGHT))  # size
    divider_block.fill(BLACK)  # Black
    run = True
    
    while run:
        clock.tick(FPS)
        events = pygame.event.get()  # Get events once per frame
        current_time = pygame.time.get_ticks()
        
        for event in events:
            if event.type == pygame.QUIT:
                run = False

        red_rect = pygame.Rect(RED_LOCATION[0], RED_LOCATION[1], SHIP_SIZE[0], SHIP_SIZE[1])
        yellow_rect = pygame.Rect(ship_location[0], ship_location[1], SHIP_SIZE[0], SHIP_SIZE[1])

        bullet_return = shoot_bullet(events)

        if bullet_return is not None:
            red_bullet -= 1
            ship_location_was = [ship_location[0], ship_location[1] + 25]
            bullets_fired.append([bullet_return, ship_location_was])

        move_bullets(bullets_fired)  # Update the movement of the bullets after they have been fired!
        move_ship(ship_location)

        red_bullet_count = font.render(f"Bullet {red_bullet}", True, WHITE)
        yellow_bullet_count = font.render(f"Bullet {yellow_bullet}", True, WHITE)

        # Check for collision between bullets and the yellow ship
        for bullet in bullets_fired:
            bullet_rect = pygame.Rect(bullet[1][0], bullet[1][1], 5, 5)
            if red_rect.colliderect(bullet_rect):
                if YELLOW_LIVES > 0:
                    YELLOW_LIVES -= 1
                bullets_fired.remove(bullet)

                # Update the lives display after a hit
                font_red_lives = font.render(F"LIVES {RED_LIVES}", True, WHITE)
                font_yellow_lives = font.render(F"LIVES {YELLOW_LIVES}", True, WHITE)

        yellow_ship_movement(location_red_ship=RED_LOCATION, location_yellow_ship=ship_location)

        # Check if it's time for the yellow ship to shoot
        if current_time - last_yellow_shot_time >= DIFFCULTY_LEVEL:  # 1000 milliseconds = 1 second
            yellow_bullet_returned = yellow_ship_shoot(location_red_ship=RED_LOCATION,
                                                       location_yellow_ship=ship_location)
            if yellow_bullet_returned is not None:
                yellow_bullet -= 1
                ship_location_was = [RED_LOCATION[0], RED_LOCATION[1] + 25]
                yellow_bullets_fired.append([yellow_bullet_returned, ship_location_was])

            last_yellow_shot_time = current_time  # Update the last shot time

        yellow_bullets_move(yellow_bullets_fired)

        for bullet in yellow_bullets_fired:  # YELLOW BULLETS RENDERING
            bullet_rect = pygame.Rect(bullet[1][0], bullet[1][1], 5, 5)
            if yellow_rect.colliderect(bullet_rect):
                if RED_LIVES > 0:
                    RED_LIVES -= 1
                yellow_bullets_fired.remove(bullet)

                # Update the lives display after a hit
                font_red_lives = font.render(F"{RED_LIVES}", True, WHITE)
                font_yellow_lives = font.render(F"{YELLOW_LIVES}", True, WHITE)

        draw_screen(divider_block,
                    background_scaled,
                    red_bullet_count,
                    yellow_bullet_count,
                    ship_location,
                    bullets_fired,
                    font_red_lives,
                    font_yellow_lives, RED_LOCATION,
                    yellow_bullets_fired)

        # Delete bullets once they get to the end of the screen
        bullets_fired = [bullet for bullet in bullets_fired if bullet[1][0] < WIDTH]  # RED BULLETS
        yellow_bullets_fired = [bullet for bullet in yellow_bullets_fired if bullet[1][0] < WIDTH]


if __name__ == "__main__":
    main()
    pygame.quit()

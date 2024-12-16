import pygame
import os
from random import randint, choice, shuffle

pygame.init()

WIDTH, HEIGHT = 900, 1200
FPS = 60

name_game = "Space Ship Shooters"
pygame.display.set_caption(name_game)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

def find_file_name(file_name):
    location = os.path.abspath(file_name)
    print("Path is :", location)

file_trajectory = "C:\\Users\\User\\OneDrive\\Documents\\VS CODE PYTHON\\features\\flappy_bird\\space invaders 2024\\assets\\"


#BACKGORUND
background = pygame.transform.scale(pygame.image.load(f"{file_trajectory}background-black.png"), (WIDTH, HEIGHT))


#PLAYER SHIP
PLAYER_WIDTH, PLAYER_HEIGHT = WIDTH // 10, HEIGHT // 10
PLAYER_SPEED = 10  
EDGE_PADDING = WIDTH // 100
MAX_LIVES = 5

player_ship = pygame.transform.scale(pygame.image.load(f"{file_trajectory}pixel_ship_yellow.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))

#LASER PROJECTILES - PLAYER
PLAYER_LASER_WIDTH, PLAYER_LASER_HEIGHT = PLAYER_WIDTH , PLAYER_HEIGHT
PLAYER_LASER_SPEED = 15

player_laser = pygame.transform.scale(pygame.image.load(f"{file_trajectory}pixel_laser_yellow.png"), (PLAYER_LASER_WIDTH, PLAYER_LASER_HEIGHT))


#ENEMIES SHIP
ENEMY_WIDTH, ENEMY_HEIGHT = PLAYER_WIDTH, PLAYER_HEIGHT
ENEMY_FALL_SPEED = 10

enemy_blue_ship = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(f"{file_trajectory}pixel_ship_blue_small.png"), (ENEMY_WIDTH, ENEMY_HEIGHT)), 180)
enemy_red_ship = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(f"{file_trajectory}pixel_ship_red_small.png"), (ENEMY_WIDTH, ENEMY_HEIGHT)), 180)
enemy_green_ship = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(f"{file_trajectory}pixel_ship_green_small.png"), (ENEMY_WIDTH, ENEMY_HEIGHT)), 180)

#LASER PROJECTILES - ENEMIES
ENEMY_LASER_WIDTH, ENEMY_LASER_HEIGHT = ENEMY_WIDTH, ENEMY_HEIGHT
ENEMY_LASER_SPEED = 15

enemy_blue_laser = pygame.transform.scale(pygame.image.load(f"{file_trajectory}pixel_laser_blue.png"), (ENEMY_LASER_WIDTH, ENEMY_LASER_HEIGHT))
enemy_red_laser = pygame.transform.scale(pygame.image.load(f"{file_trajectory}pixel_laser_red.png"), (ENEMY_LASER_WIDTH, ENEMY_LASER_HEIGHT))
enemy_green_laser = pygame.transform.scale(pygame.image.load(f"{file_trajectory}pixel_laser_green.png"), (ENEMY_LASER_WIDTH, ENEMY_LASER_HEIGHT))

enemy_ship_to_laser = {
    enemy_blue_ship : enemy_blue_laser,
    enemy_green_ship : enemy_green_laser, 
    enemy_red_ship : enemy_red_laser
}

listed_surfaces = [player_ship, player_laser, enemy_blue_ship, enemy_green_ship, enemy_red_ship, enemy_blue_laser, enemy_green_laser, enemy_red_laser]

masks = {}

for surface in listed_surfaces:
    masks[surface] = pygame.mask.from_surface(surface)

#COLOURS

RED = (200, 50, 50)
GREEN = (50, 200, 100)
WHITE = (255, 255, 255)


def get_laser_xcor(cooldown, player_xcor, max_cooldown, laser_xcor):
    if cooldown == max_cooldown:
        return player_xcor
    else:
        return laser_xcor
    

def send_wave(wave_count):
    wave_count += 1
    num_enemies = randint(wave_count + 3, wave_count * 2 + 3)

    xcors = [cor for cor in range(EDGE_PADDING, WIDTH - ENEMY_WIDTH - EDGE_PADDING, ENEMY_WIDTH)]
    ycors = [cor for cor in range(HEIGHT * -1, 0 - ENEMY_HEIGHT, ENEMY_HEIGHT)]

    #combined_cors = [[xcor]]
    shuffle(xcors)
    shuffle(ycors)

    enemies = []
    for _ in range(num_enemies):
        enemies.append([choice(list(enemy_ship_to_laser.keys())), xcors.pop(), ycors.pop()])

    return wave_count, enemies

def main():
    game = True
    fps_clock = pygame.time.Clock()

    player_xcor = WIDTH / 2 - PLAYER_WIDTH / 2 #default / start position
    PLAYER_YCOR = HEIGHT - 200
    PLAYER_LASER_HEALTH_PADDING = HEIGHT / 100

    lives_count = MAX_LIVES
    lives_waves_font = pygame.font.SysFont("arial", WIDTH // 20)

    PLAYER_MAX_HP = 100
    health_lost = 0
    health_lost_display = health_lost / PLAYER_MAX_HP * PLAYER_WIDTH 

    COOLDWON_CAP = 60
    cooldown = COOLDWON_CAP
    laser_activated = False
    laser_y = PLAYER_YCOR - PLAYER_LASER_HEALTH_PADDING
    laser_xcor = None

    wave_count = 0
    wave_passed = True

    while game:
        fps_clock.tick(FPS)

        WIN.blit(background, (0,0))

        if wave_passed:
            wave_count, listed_enemy_xycors = send_wave(wave_count)
            list_ycors = [y_value[2] for y_value in listed_enemy_xycors]
            highest_enemy_level = min(list_ycors)

            wave_passed = False

        if highest_enemy_level > HEIGHT :

            #print(f"Yes, {highest_enemy_level} > {HEIGHT}")
            wave_passed = True
            listed_enemy_xycors = None
            highest_enemy_level = 0
        else:
            for enemy_count, enemy_list in enumerate(listed_enemy_xycors.copy()):
                #print(highest_enemy_level)
                WIN.blit(enemy_list[0], (enemy_list[1], enemy_list[2]))
                listed_enemy_xycors[enemy_count][2] += ENEMY_FALL_SPEED
                
            highest_enemy_level += ENEMY_FALL_SPEED

        #for i in range(3):
        #a    WIN.blit(list(enemy_ship_to_laser.values())[i], (100*i, 100))

        lives_text = lives_waves_font.render(f"Lives: {'♥ ' * lives_count}", True, WHITE)
        WIN.blit(lives_text, (WIDTH / 2 - lives_text.get_width() / 2, EDGE_PADDING))

        waves_text = lives_waves_font.render(f"Waves cleared: {wave_count}", True, WHITE)
        WIN.blit(waves_text, (WIDTH / 2 - waves_text.get_width() / 2, EDGE_PADDING + lives_text.get_height()))

        if laser_activated:
            laser_xcor = get_laser_xcor(cooldown, player_xcor, COOLDWON_CAP, laser_xcor)
            laser_y -= PLAYER_LASER_SPEED
            WIN.blit(player_laser, (laser_xcor, laser_y))
            cooldown -= 1
            if cooldown == 0 or laser_y < 0 - PLAYER_LASER_HEIGHT:
                cooldown = COOLDWON_CAP
                laser_y = PLAYER_YCOR - PLAYER_LASER_HEALTH_PADDING
                laser_activated = False

        WIN.blit(player_ship, (player_xcor, PLAYER_YCOR))
        
        health_bar_underneath = pygame.rect.Rect(player_xcor, PLAYER_YCOR + PLAYER_HEIGHT + PLAYER_LASER_HEALTH_PADDING, PLAYER_WIDTH, PLAYER_LASER_HEALTH_PADDING)
        health_bar_display = pygame.rect.Rect(player_xcor, PLAYER_YCOR + PLAYER_HEIGHT + PLAYER_LASER_HEALTH_PADDING, PLAYER_WIDTH - health_lost_display, PLAYER_LASER_HEALTH_PADDING)

        pygame.draw.rect(WIN, RED, health_bar_underneath)
        pygame.draw.rect(WIN, GREEN, health_bar_display)

        keys_pressed = pygame.key.get_pressed()

        if (keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]) and player_xcor > EDGE_PADDING:
            player_xcor -= PLAYER_SPEED
        if (keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]) and player_xcor < WIDTH - PLAYER_WIDTH - EDGE_PADDING:
            player_xcor += PLAYER_SPEED
        if keys_pressed[pygame.K_SPACE] and not laser_activated:
            laser_activated = True

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                break

    pygame.quit()
    quit("Thanks for playing")



if __name__ == "__main__":
    main()
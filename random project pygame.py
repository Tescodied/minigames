import pygame
from random import shuffle, choice, randint
from time import sleep

pygame.init()

FPS = 60
WIDTH, HEIGHT = 900, 900 # I found 900, 900 ideal
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))

PLAYER_GAP = WIDTH // 10 #between bottom of screen and player
PLAYER_WIDTH, PLAYER_HEIGHT = WIDTH // 15, HEIGHT // 15
PLAYER_SPEED = 10
PLAYER_OUTLINE = 5
PLAYER_COLOUR = (0, 200, 255)
PLAYER_OUTLINE_COLOUR = (255, 255, 255)
player_lives = 5
PLAYER_LIVES_MAX = player_lives

ENEMY_WIDTH, ENEMY_HEIGHT = int(PLAYER_WIDTH // 1.5), int(PLAYER_HEIGHT // 1.5)
ENEMY_SPAWN_HEIGHT_RANGES = (HEIGHT // 20, HEIGHT // 10)
ENEMIES_COLOUR = (200, 50, 50)
ENEMY_FALL_RATE = 10
ENEMY_PADDING = HEIGHT // 100

BLACK =         (0,0,0)
WHITE =         (255,255,255)
GREEN =         (0, 200, 100)
AMBER =         (255, 150, 0)
RED =           (255,50,50)
DARK_BLUE =     (100, 100, 255)
LIGHT_RED =     (255, 10, 100)
LIGHT_GREY =    (50, 50, 50)

BAR_COLOR = GREEN
BAR_WIDTH = ENEMY_WIDTH // 2
BAR_HEIGHT = ENEMY_HEIGHT // 2

def quit_game():
    quit("Thanks for playing")

def calc_text_padding(options_text):
    padding = 0

    for text in options_text:
        padding += text.get_width()

    return (WIDTH - padding) / (len(options_text) + 1)


def get_difficulty(clock):
    MAIN_FONT_SIZE = WIDTH // 10
    OPTIONS_FONT_SIZES = MAIN_FONT_SIZE // 2
    OUTLINE_DIST = 10

    main_font = pygame.font.SysFont("Arial", MAIN_FONT_SIZE)
    options_font = pygame.font.SysFont("Arial", OPTIONS_FONT_SIZES)

    welcome_text = main_font.render("BLOCK DODGE", True, LIGHT_RED)
    main_text = main_font.render("Select a difficulty", True, WHITE)

    options = {"Easy":GREEN,  "Medium": AMBER, "Hard": RED, "Impossible": DARK_BLUE}
    options_text = []

    for key, value in options.items():
        options_text.append(options_font.render(key, True, value))

    
    control_ycor_difficulties = HEIGHT * (8/10)

    choosing = True

    while choosing:
        clock.tick(FPS)

        difficulties_x = []

        SCREEN.fill(BLACK)

        SCREEN.blit(welcome_text, (WIDTH // 2 - welcome_text.get_width() // 2, HEIGHT // 10))
        SCREEN.blit(main_text, (WIDTH // 2 - main_text.get_width() // 2, HEIGHT // 5))

        PADDING = calc_text_padding(options_text)

        for index, difficulty in enumerate(options_text):
            cumulative_width = sum(text.get_width() for text in options_text[:index])

            independent_xcor = PADDING * (index + 1) + cumulative_width
            difficulties_x.append(independent_xcor)

            pygame.draw.rect(SCREEN, WHITE, (independent_xcor - OUTLINE_DIST, control_ycor_difficulties - OUTLINE_DIST, difficulty.get_width() + OUTLINE_DIST * 2, difficulty.get_height() + OUTLINE_DIST * 2))
            pygame.draw.rect(SCREEN, BLACK, (independent_xcor - OUTLINE_DIST / 2, control_ycor_difficulties - OUTLINE_DIST / 2, difficulty.get_width() + OUTLINE_DIST, difficulty.get_height() + OUTLINE_DIST))

            SCREEN.blit(difficulty, (independent_xcor, control_ycor_difficulties))

        pygame.display.update()

        

        xpos, ypos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for index, (difficulty, xcor) in enumerate(zip(options_text, difficulties_x)):
                    if xcor - PLAYER_OUTLINE <= xpos <= xcor + difficulty.get_width() + OUTLINE_DIST and control_ycor_difficulties <= ypos <= control_ycor_difficulties + difficulty.get_height():
                        return  index * 2 + 5, list(options.values())[index]
                    

def loading(speed_clock):
    counter_list = [index for index in range(1,4) for _ in range(60)]
    LENGTH_COUNTER_LIST = len(counter_list) - 1 

    counter = LENGTH_COUNTER_LIST
    counter_font = pygame.font.SysFont("Verdana", WIDTH // 5)

    while counter >= 0:
        speed_clock.tick(FPS)

        SCREEN.fill(BLACK)

        counter_text = counter_font.render(str(counter_list[counter]), True, WHITE)
        SCREEN.blit(counter_text, (WIDTH // 2 - counter_text.get_width() // 2, HEIGHT // 2 - counter_text.get_height() // 2))

        counter -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        pygame.display.update()


def summon_enemies(enemies, NUM_ENEMIES, xcors_list, ycors_list):
    for _ in range(NUM_ENEMIES):
        enemies.append(pygame.rect.Rect(xcors_list.pop(), choice(ycors_list), ENEMY_WIDTH, ENEMY_HEIGHT))

    return enemies


def summon_bars(health_bars, NUM_ENEMIES, xcors_list, y_cors_list):
    num_bars = randint(1, NUM_ENEMIES // 2)
    for _ in range(num_bars):
        health_bars.append(pygame.rect.Rect(xcors_list.pop(), choice(y_cors_list), BAR_WIDTH, BAR_HEIGHT))

    return health_bars


def main():
    global player_lives
    running = True
    speed_clock = pygame.time.Clock()

    player_xcor = WIDTH // 2 - PLAYER_WIDTH // 2 # starting / default position
    player_ycor = HEIGHT - PLAYER_GAP

    enemies = []
    enemies_mask = []

    health_bars = []

    lives_text_font = pygame.font.SysFont("Arial", WIDTH // 30)
    score_text_font = pygame.font.SysFont("Arial", WIDTH // 20)

    score = -1
    
    TEXT_PADDING = HEIGHT // 100

    NUM_ENEMIES, CHOSEN_COLOUR = get_difficulty(speed_clock)
    loading(speed_clock)

    while running:
        speed_clock.tick(FPS)

        SCREEN.fill(BLACK)

        ##DRAWS PLAYER AREA
        player_area = pygame.rect.Rect(0,HEIGHT // 2, WIDTH, HEIGHT // 2)
        pygame.draw.rect(SCREEN, LIGHT_GREY, player_area)

        ##DRAWS PLAYER
        player_rect = pygame.rect.Rect(player_xcor, player_ycor, PLAYER_WIDTH, PLAYER_HEIGHT)
        player_mask_outline = pygame.rect.Rect(player_xcor - PLAYER_OUTLINE , player_rect.y - PLAYER_OUTLINE, PLAYER_WIDTH + PLAYER_OUTLINE * 2, PLAYER_HEIGHT + PLAYER_OUTLINE * 2)

        pygame.draw.rect(SCREEN, PLAYER_OUTLINE_COLOUR, player_mask_outline)
        pygame.draw.rect(SCREEN, PLAYER_COLOUR, player_rect)

        ##DRAWS ENEMIES
        if len(enemies) > 0:
            for enemy in enemies:
                if enemy.y < HEIGHT:
                    enemy.y += ENEMY_FALL_RATE
                    pygame.draw.rect(SCREEN, ENEMIES_COLOUR, enemy)

                    if player_mask_outline.colliderect(enemy):
                        player_lives -= 1
                        enemies.remove(enemy)
                else:
                    enemies.remove(enemy)   
        else:
            score += 1
            enemy_listed_xcors = [index for index in range(0, WIDTH - ENEMY_WIDTH, ENEMY_WIDTH)]
            enemy_listed_ycors = [index for index in range(ENEMY_SPAWN_HEIGHT_RANGES[0], ENEMY_SPAWN_HEIGHT_RANGES[1], ENEMY_PADDING)]
            
            shuffle(enemy_listed_xcors)

            enemies = summon_enemies(enemies, NUM_ENEMIES, enemy_listed_xcors, enemy_listed_ycors)

        score_display = score_text_font.render(f"Score: {score}", True, WHITE)
        lives_display = lives_text_font.render(f"Lives: {'♥ ' * player_lives}", True, WHITE)

        ##DRAWS LIVES AND SCORE
        SCREEN.blit(lives_display, (WIDTH // 100, TEXT_PADDING))   
        SCREEN.blit(score_display, (WIDTH // 2 - score_display.get_width() // 2, TEXT_PADDING))

        ##DRAWS HEALTH BOOSTS
        if len(health_bars) > 0:
            for bar in health_bars:
                if bar.y < HEIGHT:
                    bar.y += ENEMY_FALL_RATE
                    pygame.draw.rect(SCREEN, BAR_COLOR, bar)

                    if player_mask_outline.colliderect(bar) and player_lives < PLAYER_LIVES_MAX:
                        player_lives += 1
                        health_bars.remove(bar)
                else:
                    health_bars.remove(bar)   
        else:
            health_listed_xcors = [index for index in range(0, WIDTH - ENEMY_WIDTH, ENEMY_WIDTH)]
            health_listed_ycors = [index for index in range(ENEMY_SPAWN_HEIGHT_RANGES[0], ENEMY_SPAWN_HEIGHT_RANGES[1], ENEMY_PADDING)]
            
            shuffle(health_listed_xcors)

            health_bars = summon_bars(health_bars, NUM_ENEMIES, health_listed_xcors, health_listed_ycors)

        if player_lives == 0:
            sleep(1)
            SCREEN.fill(BLACK)

            losing_text_font = pygame.font.SysFont("Verdana", WIDTH // 10)

            you_lost_text = losing_text_font.render("You lost!", False, WHITE)
            score_text = losing_text_font.render(f"Your score was {score}", False, CHOSEN_COLOUR)

            SCREEN.blit(you_lost_text, 
                        (WIDTH // 2 - you_lost_text.get_width() // 2, 
                        HEIGHT // 3 - you_lost_text.get_height() // 2))
            
            SCREEN.blit(score_text, 
                        (WIDTH // 2 - score_text.get_width() // 2, 
                        HEIGHT // 1.5 - score_text.get_height() // 2))
            
            pygame.display.update()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit_game()
            
        pygame.display.update()

        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_LEFT] and player_mask_outline.left > PLAYER_OUTLINE * 2:
            player_xcor -= PLAYER_SPEED
            
        if keys_pressed[pygame.K_RIGHT] and player_mask_outline.left < WIDTH - (player_mask_outline.width + PLAYER_OUTLINE):
            player_xcor += PLAYER_SPEED

        if keys_pressed[pygame.K_UP] and player_mask_outline.top > player_area.top + PLAYER_OUTLINE * 2:
            player_ycor -= PLAYER_SPEED

        if keys_pressed[pygame.K_DOWN] and player_mask_outline.top < HEIGHT - (player_mask_outline.height + PLAYER_OUTLINE):
            player_ycor += PLAYER_SPEED

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
 

if __name__ == "__main__":
    main()

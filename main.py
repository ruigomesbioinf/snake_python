import pygame
import random

# SET DISPLAY 
pygame.init()
display_width = 400
display_height = 300
display = pygame.display.set_mode((display_width, display_height))
snake_icon = pygame.image.load("C:/Users/geral/desktop/SNAKE_PYTHON/assets/snake.png")
pygame.display.set_icon(snake_icon)
pygame.display.set_caption("snake.py - A Python Adventure")
clock = pygame.time.Clock()

# COLORS
VERDE_AGUA = (127, 255, 212)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (72, 124, 39)
BROWN = (255,248,220)

def game_intro():
    intro = True
    while intro:

        # MUSIC
        pygame.mixer.init()
        pygame.mixer.music.load("C:/Users/geral/desktop/SNAKE_PYTHON/assets/main_menu.mp3")
        pygame.mixer.music.play(-1)

        # LOGIC TO END GAME IN INTRO
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.fill(WHITE)

        # SET INTRO DISPLAY
        # LOGOTYPE
        snakepy_logo = pygame.image.load("C:/Users/geral/desktop/SNAKE_PYTHON/assets/snakepy.png")
        snakepy_logo_rect = snakepy_logo.get_rect()
        snakepy_logo_rect.center = (display_width // 2, display_height // 2)
        display.blit(snakepy_logo, snakepy_logo_rect)

        # "BUTTONS" LOGIC
        mouse = pygame.mouse.get_pos()
        if 75+100 > mouse[0] > 75 and 200+35 > mouse[1] > 200:
            pygame.draw.rect(display, GREEN, (75, 200, 100, 35))

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_loop()
        else:
            pygame.draw.rect(display, VERDE_AGUA, (75, 200, 100, 35))

        if 225+100 > mouse[0] > 225 and 200+35 > mouse[1] > 200:
            pygame.draw.rect(display, GREEN, (225, 200, 100, 35))

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.quit()
                    quit()
        else:
            pygame.draw.rect(display, VERDE_AGUA, (225, 200, 100, 35))

        # PLAY BUTTON
        button_font = pygame.font.SysFont(None, 20)
        button_play = button_font.render("PLAY", True, BLACK)
        button_play_rect = button_play.get_rect()
        button_play_rect.center = ( (75 + (100 / 2)) , (200 + (35 / 2)) )
        display.blit(button_play, button_play_rect)

        # EXIT BUTTON
        button_exit = button_font.render("EXIT", True, BLACK)
        button_exit_rect = button_exit.get_rect()
        button_exit_rect.center = ( (225 + (100 / 2)) , (200 + (35 / 2)) )
        display.blit(button_exit, button_exit_rect)
        pygame.display.update()


def game_over_message(message, color1, color2):
    '''
    Function that render in-game "game over" message.
    '''
    font = pygame.font.SysFont(None, 25) # font object, first arg name, second arg size
    text = font.render(message, True, color1, color2) # text surface to draw in
    text_rect = text.get_rect() # rectangle object of text
    text_rect.center = (display_width // 2, display_height // 2) # adjust to the center of screen
    display.blit(text, text_rect) # display text on screen
    pygame.display.update()

def score_display(score):
    '''
    Function that render and display in screen the player score
    '''
    score_font = pygame.font.SysFont(None, 20)
    value = score_font.render("Score: " + str(score), True, VERDE_AGUA)
    display.blit(value, [0, 0])

def snake_increase_size(snake_block, snake_list):
    '''
    Function that draws another rectangle when the snake collides with food, increasing the snake size.
    '''
    for x in snake_list:
        pygame.draw.rect(display, GREEN, [x[0], x[1], snake_block, snake_block])

# MAIN LOOP
def game_loop():
    game_over = False # main variable to make the while loop work
    game_closed = False
    score = 0

    # SNAKE ATRIBUTES
    X = 200
    Y = 150
    Y_CHANGE = 0
    X_CHANGE = 0
    SNAKE_SPEED = 10
    SNAKE_SIZE = 10
    snake_list = []
    lenght_of_snake = 1

    # FOOD ATRIBUTES
    foodx = round(random.randrange(0, display_width - SNAKE_SIZE) / 10 ) * 10.0
    foody = round(random.randrange(0, display_height - SNAKE_SIZE) / 10 ) * 10.0

    while not game_over:
        
        # WHILE LOOP FOR THE PLAYER TO DECIDE IF HE WANTS TO CONTINUE OR QUIT GAME
        while game_closed == True:
            display.fill(BLACK)
            score_display(score)
            game_over_message("You lost! Press C-Continue playing or Q-quit.", BLACK, WHITE)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_closed = False
                    if event.key == pygame.K_c:
                        game_loop()

        # SNAKE MOVEMENT LOGIC
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    X_CHANGE = -SNAKE_SIZE
                    Y_CHANGE = 0
                elif event.key == pygame.K_RIGHT:
                    X_CHANGE = SNAKE_SIZE
                    Y_CHANGE = 0
                elif event.key == pygame.K_UP:
                    Y_CHANGE = -SNAKE_SIZE
                    X_CHANGE = 0
                elif event.key == pygame.K_DOWN:
                    Y_CHANGE = SNAKE_SIZE
                    X_CHANGE = 0
        
        X += X_CHANGE
        Y += Y_CHANGE
        display.fill(BLACK)
        pygame.draw.rect(display, BROWN, [foodx, foody, SNAKE_SIZE, SNAKE_SIZE])
        pygame.draw.rect(display, GREEN, [X, Y, SNAKE_SIZE, SNAKE_SIZE])
        score_display(score)

        # SNAKE INCREASING LOGIC
        snake_head = []
        snake_head.append(X)
        snake_head.append(Y)
        snake_list.append(snake_head)
        if len(snake_list) > lenght_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_closed = True
        snake_increase_size(SNAKE_SIZE, snake_list)

        pygame.display.update()

        # SNAKE COLLIDING WITH WALLS AND FOOD LOGIC
        if X >= display_width or X < 0 or Y >= display_height or Y < 0:
            game_closed = True

        snake_rect = pygame.Rect(X, Y, SNAKE_SIZE, SNAKE_SIZE)
        food_rect = pygame.Rect(foodx, foody, SNAKE_SIZE, SNAKE_SIZE)

        if snake_rect.colliderect(food_rect):
            score += 1
            foodx = round(random.randrange(0, display_width - SNAKE_SIZE) / 10) * 10.0
            foody = round(random.randrange(0, display_height - SNAKE_SIZE) / 10) * 10.0
            SNAKE_SPEED += 1
            lenght_of_snake += 1

        
        clock.tick(SNAKE_SPEED)


    # ending game
    pygame.quit()
    quit()

game_intro()
# game_loop()
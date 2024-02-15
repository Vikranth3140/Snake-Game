import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Set up colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Set up the Snake
block_size = 20
snake_speed = 10

font = pygame.font.SysFont(None, 40)


def snake(block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], block_size, block_size])


def message_to_screen(msg, color):
    screen_text = font.render(msg, True, color)
    screen.blit(screen_text, [SCREEN_WIDTH / 6, SCREEN_HEIGHT / 3])


def gameLoop():
    global snake_speed  # Declare snake_speed as global variable

    game_over = False
    game_close = False

    lead_x = SCREEN_WIDTH / 2
    lead_y = SCREEN_HEIGHT / 2

    lead_x_change = 0
    lead_y_change = 0

    snake_list = []
    snake_length = 1

    randAppleX = round(random.randrange(0, SCREEN_WIDTH - block_size) / block_size) * block_size
    randAppleY = round(random.randrange(0, SCREEN_HEIGHT - block_size) / block_size) * block_size

    while not game_over:

        while game_close:
            screen.fill(WHITE)
            message_to_screen("You lost! Press C-Play Again or Q-Quit", RED)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    lead_y_change = block_size
                    lead_x_change = 0

        if lead_x >= SCREEN_WIDTH or lead_x < 0 or lead_y >= SCREEN_HEIGHT or lead_y < 0:
            game_close = True
        lead_x += lead_x_change
        lead_y += lead_y_change
        screen.fill(WHITE)
        pygame.draw.rect(screen, RED, [randAppleX, randAppleY, block_size, block_size])
        snake_head = []
        snake_head.append(lead_x)
        snake_head.append(lead_y)
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        snake(block_size, snake_list)

        pygame.display.update()

        if lead_x == randAppleX and lead_y == randAppleY:
            randAppleX = round(random.randrange(0, SCREEN_WIDTH - block_size) / block_size) * block_size
            randAppleY = round(random.randrange(0, SCREEN_HEIGHT - block_size) / block_size) * block_size
            snake_length += 1
            # Increase snake speed as it grows
            snake_speed += 1

        # Display score
        score = snake_length - 1
        score_text = font.render("Score: " + str(score), True, BLACK)
        screen.blit(score_text, [10, 10])

        pygame.display.update()

        pygame.time.Clock().tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()
import pygame
import random

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLACK = (0, 0, 0)
        self.block_size = 20
        self.snake_speed = 10
        self.font = pygame.font.SysFont(None, 40)
        self.paused = False
        self.pause_icon = pygame.image.load("images/pause.png")
        self.play_icon = pygame.image.load("images/play.png")
        self.pause_icon = pygame.transform.scale(self.pause_icon, (int(self.SCREEN_WIDTH * 0.05), int(self.SCREEN_WIDTH * 0.05)))
        self.play_icon = pygame.transform.scale(self.play_icon, (int(self.SCREEN_WIDTH * 0.05), int(self.SCREEN_WIDTH * 0.05)))
        self.pause_icon_rect = self.pause_icon.get_rect(topright=(self.SCREEN_WIDTH - 10, 10))
        self.block_colors = [(26, 32, 100), (255, 0, 0), (139, 69, 19), (138, 43, 226), (54, 69, 79)]

    def draw_snake(self, snake_list):
        for x in snake_list:
            pygame.draw.rect(self.screen, self.GREEN, [x[0], x[1], self.block_size, self.block_size])

    def display_message(self, msg, color, y_displacement=0):
        screen_text = self.font.render(msg, True, color)
        text_rect = screen_text.get_rect(center=(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2 + y_displacement))
        self.screen.blit(screen_text, text_rect)

    def game_loop(self):
        game_over = False
        game_close = False
        lead_x = self.SCREEN_WIDTH / 2
        lead_y = self.SCREEN_HEIGHT / 2
        lead_x_change = 0
        lead_y_change = 0
        snake_list = []
        snake_length = 1

        num_blocks = 8
        block_positions = [(random.randrange(0, self.SCREEN_WIDTH - self.block_size, self.block_size),
                            random.randrange(0, self.SCREEN_HEIGHT - self.block_size, self.block_size)) for _ in range(num_blocks)]
        block_colors = random.choices(self.block_colors, k=num_blocks)

        while not game_over:
            while game_close:
                self.screen.fill(self.WHITE)
                self.display_message("You lost! Press C-Play Again or Q-Quit", self.RED, y_displacement=-50)
                self.display_message("Score: " + str(snake_length - 1), self.BLACK, y_displacement=50)
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
                            self.game_loop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        lead_x_change = -self.block_size
                        lead_y_change = 0
                    elif event.key == pygame.K_RIGHT:
                        lead_x_change = self.block_size
                        lead_y_change = 0
                    elif event.key == pygame.K_UP:
                        lead_y_change = -self.block_size
                        lead_x_change = 0
                    elif event.key == pygame.K_DOWN:
                        lead_y_change = self.block_size
                        lead_x_change = 0
                    elif event.key == pygame.K_p:
                        self.paused = not self.paused

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.pause_icon_rect.collidepoint(mouse_pos):
                        self.paused = not self.paused

            if not self.paused:
                lead_x += lead_x_change
                lead_y += lead_y_change
                lead_x %= self.SCREEN_WIDTH
                lead_y %= self.SCREEN_HEIGHT

                self.screen.fill(self.WHITE)
                pygame.draw.rect(self.screen, self.RED, [lead_x, lead_y, self.block_size, self.block_size])
                for i, block_pos in enumerate(block_positions):
                    pygame.draw.rect(self.screen, block_colors[i], [block_pos[0], block_pos[1], self.block_size, self.block_size])

                snake_head = []
                snake_head.append(lead_x)
                snake_head.append(lead_y)
                snake_list.append(snake_head)
                if len(snake_list) > snake_length:
                    del snake_list[0]

                for x in snake_list[:-1]:
                    if x == snake_head:
                        game_close = True

                self.draw_snake(snake_list)

                score_text = self.font.render("Score: " + str(snake_length - 1), True, self.BLACK)
                self.screen.blit(score_text, [10, 10])

                self.pause_icon_rect = self.pause_icon.get_rect(topright=(self.SCREEN_WIDTH - 10, 10))
                if self.paused or game_close:
                    self.screen.blit(self.play_icon, self.pause_icon_rect)
                else:
                    self.screen.blit(self.pause_icon, self.pause_icon_rect)

                pygame.display.update()

                for i, block_pos in enumerate(block_positions[:]):
                    if snake_head[0] == block_pos[0] and snake_head[1] == block_pos[1]:
                        snake_length += 1
                        self.snake_speed += 1
                        block_positions.remove(block_pos)
                        block_colors.pop(i)
                        block_positions.append((random.randrange(0, self.SCREEN_WIDTH - self.block_size, self.block_size),
                                                random.randrange(0, self.SCREEN_HEIGHT - self.block_size, self.block_size)))
                        block_colors.append(random.choice(self.block_colors))

                pygame.time.Clock().tick(self.snake_speed)

        pygame.quit()
        quit()

game = SnakeGame()
game.game_loop()
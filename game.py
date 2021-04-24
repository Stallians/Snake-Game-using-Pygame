import pygame
from random import randint, randrange
import time
from pygame.locals import *

SIZE = 25
MAX_X = 500
MAX_Y = 500


class Apple:
    def __init__(self, parent_surface):
        self.parent_surface = parent_surface
        self.image = pygame.image.load("./Resources/apple.png").convert()
        self.image = pygame.transform.scale(self.image, (SIZE, SIZE))
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.parent_surface.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def get_apple_position(self):
        return (self.x, self.y)

    def get_new_apple(self):
        self.x = randrange(0, MAX_X - 1, SIZE)
        self.y = randrange(0, MAX_Y - 1, SIZE)


class Snake:
    def __init__(self, parent_surface, length=1):
        self.length = length
        self.block = pygame.image.load("./Resources/square.png").convert()
        self.block = pygame.transform.scale(self.block, (SIZE, SIZE))
        self.surface = parent_surface
        self.x = [SIZE] + [-1] * (length - 1)
        self.y = [SIZE] + [-1] * (length - 1)
        self.direction = "right"

    def draw(self):
        self.surface.fill((69, 252, 3))
        for i in range(self.length):
            self.surface.blit(self.block, (self.x[i], self.y[i]))

    def move_down(self):
        self.direction = "down"

    def move_up(self):
        self.direction = "up"

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "right":
            self.x[0] += SIZE
        elif self.direction == "left":
            self.x[0] -= SIZE
        elif self.direction == "up":
            self.y[0] -= SIZE
        elif self.direction == "down":
            self.y[0] += SIZE

        if self.x[0] < 0 or self.x[0] >= MAX_X:
            self.x[0] = (self.x[0] + MAX_X) % MAX_X
        if self.y[0] < 0 or self.y[0] >= MAX_Y:
            self.y[0] = (self.y[0] + MAX_Y) % MAX_Y
        self.draw()

    def grow_snake(self):
        self.x.append(self.x[-1])
        self.y.append(self.y[-1])
        self.length += 1

    def get_snake_position(self):
        return (self.x[0], self.y[0])


class Game:
    def __init__(self):
        pygame.init()
        self.parent_surface = pygame.display.set_mode((MAX_X, MAX_Y))
        self.parent_surface.fill((69, 252, 3))
        self.snake = Snake(self.parent_surface, 5)
        self.apple = Apple(self.parent_surface)

    def play(self):
        self.snake.walk()
        self.detect_snake_body()
        self.detect_apple()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

    def detect_snake_body(self):
        snake_head_pos = self.snake.get_snake_position()
        for body_pos in zip(self.snake.x[3:], self.snake.y[3:]):
            if body_pos == snake_head_pos:
                raise "Game Over"

    def detect_apple(self):
        if self.snake.get_snake_position() == self.apple.get_apple_position():
            self.snake.grow_snake()
            self.apple.get_new_apple()

    def display_score(self):
        font = pygame.font.SysFont("arial", SIZE)
        score = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.parent_surface.blit(score, (400, 10))

    def display_pause_screen(self):
        font = pygame.font.SysFont("arial", 20)
        score = font.render(
            f"Oops! Snake bit himself. Press 'Enter' to restart. ",
            True,
            (255, 255, 255),
        )
        self.parent_surface.fill((69, 252, 3))
        self.parent_surface.blit(score, (50, 250))
        pygame.display.flip()

    def run(self):
        running = True
        pause = False
        while running:
            time.sleep(0.1)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if not pause:
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        elif event.key == K_UP:
                            self.snake.move_up()
                        elif event.key == K_LEFT:
                            self.snake.move_left()
                        elif event.key == K_RIGHT:
                            self.snake.move_right()
                    elif event.key == K_RETURN:
                        pause = False
                        self.snake = Snake(self.parent_surface, 5)
                        self.apple = Apple(self.parent_surface)
                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception:
                pause = True
                self.display_pause_screen()


if __name__ == "__main__":
    game = Game()
    game.run()

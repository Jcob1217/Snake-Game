import pygame
import random
import numpy as np

pygame.init()

# Setting constant variables
resolution = (width, height) = (800, 800)
color = (0, 0, 0)
white = (255, 255, 255)
green = (30, 170, 30)
positions = np.arange(0, 800, 40)
fail = False

# Initialise pygame window
pygame.display.set_caption("Snake Game")
screen = pygame.display.set_mode(resolution)
screen.fill(color)


class Apple(): 
    def __init__(self, x, y):
        self.position([x], [y])

    # Drawing apple on the screen
    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.x, self.y, 40, 40))
        pygame.display.update()
        
    # Selecting appropriate position for apple
    def position(self, body_x, body_y):
        body = []
        for (x, y) in zip(body_x, body_y):
            body.append([x, y])

        # Checking if apple random position is not inside of one of snake's segments
        while True:
            self.pos = np.random.choice(positions, 2).tolist()
            if self.pos not in body:
                break

        self.x, self.y = self.pos


class Snake():
    def __init__(self, size):
        self.size = size
        self.width = self.height = size
        self.x = [np.random.choice(positions)]
        self.y = [np.random.choice(positions)]
        self.head = [self.x[0], self.y[0]]
        self.last = random.choice(["up", "down", "left", "right"])
        self.length = 1

    # Moving the snake forward
    def foward_movement(self):
        if self.last == "up":
            self.head[1] -= self.height
        elif self.last == "down":
            self.head[1] += self.height
        elif self.last == "left":
            self.head[0] -= self.width
        elif self.last == "right":
            self.head[0] += self.width

    # Snake eating mechanism
    def eat(self, apple):
        apple.position(self.x, self.y)
        self.add_segment()
        print(f"Score: {self.length}")

    # Creating end game window after failing
    def end_game(self):
        screen.fill(green)
        font = pygame.font.Font('freesansbold.ttf', 48)
        text = font.render('Game Over!', True, white, green)
        textRect = text.get_rect()
        textRect.center = (width // 2, height // 2)
        screen.blit(text, textRect)

    # Drawing snake on the screen
    def draw(self):
        self.turn()
        self.foward_movement()
        self.check_collision()

        # Drawing snake segments 
        for i in range(self.length):
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.x[i], self.y[i], self.width, self.height))

    # Making snake body follow the head
    def turn(self):
        temp = self.x.copy()
        self.x = [temp[i - 1] if i != 0 else self.head[0] for i in range(self.length)]

        temp = self.y.copy()
        self.y = [temp[i - 1] if i != 0 else self.head[1] for i in range(self.length)]

    # Adding snake segment after eating apple
    def add_segment(self):
        self.length += 1
        self.x.append(self.x[-1] + width)
        self.y.append(self.y[-1] + height)

    def check_collision(self):
        for i in range(1, self.length):
            if self.head[0] == self.x[i] and self.head[1] == self.y[i]:
                global fail
                fail = True
                
        # Moving snake to the opposite side of the screen after getting out of bounds
        if self.head[0] > width - self.size:
            self.head[0] = 0
        elif self.head[0] < 0:
            self.head[0] = width - self.size
        if self.head[1] > height - self.size:
            self.head[1] = 0
        elif self.head[1] < 0:
            self.head[1] = height - self.size

# Drawing game elements onto the screen
def draw(snake, apple):
    # Checking if snake's head hit it's body
    if fail == False:
        screen.fill(color)
        snake.draw()
        # Checking if snake ate the apple
        if [snake.head[0], snake.head[1]] == apple.pos:
            snake.eat(apple)
        apple.draw()
        pygame.time.wait(100)
    else:
        snake.end_game()

    pygame.display.update()

snake = Snake(40)
apple = Apple(200, 200)
running = True
while running:
    for event in pygame.event.get():
        # Creating event to quit the game
        if event.type == pygame.QUIT:
            running = False
        # Checking whenever a key is pressed down
        if event.type == pygame.KEYDOWN:
            if event.key in  [pygame.K_w, pygame.K_UP] and snake.last != "down": 
                snake.last = "up"     
            elif event.key in [pygame.K_s, pygame.K_DOWN] and snake.last != "up":
                snake.last = "down"      
            elif event.key in [pygame.K_a, pygame.K_LEFT] and snake.last != "right":
                snake.last = "left"      
            elif event.key in [pygame.K_d, pygame.K_RIGHT] and snake.last != "left":
                snake.last = "right"       

    draw(snake, apple)

    
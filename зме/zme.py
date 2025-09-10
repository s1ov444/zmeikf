from pygame import *
from time import time as timer
from random import *

WIDIH, HEIGHT = 750, 500
SQUARE_SIZE = 50
FPS = 60

font.init()
game_font = font.Font(None, 50)
text = game_font.render('You lose)', True, (225, 0, 0))

W = display.set_mode((WIDIH, HEIGHT))
display.set_caption('Змейка')

bg = transform.scale(image.load('background.jpg'), (WIDIH, HEIGHT))

class GameSprite(sprite.Sprite):
    def __init__(self, pl_image, pl_x, pl_y):
        super().__init__()
        self.image = transform.scale(image.load(pl_image), (SQUARE_SIZE, SQUARE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = pl_x
        self.rect.y = pl_y

    def draw_sprite(self):
        W.blit(self.image, (self.rect.x, self.rect.y))

class Snake(GameSprite):
    def __init__(self, pl_image, pl_x, pl_y):
        super().__init__(pl_image, pl_x, pl_y)
        self.dx = SQUARE_SIZE
        self.dy = 0
    def update(self):
        for i in range(len(snake) - 1, 0, -1):
            snake[i].rect.x = snake[i - 1].rect.x
            snake[i].rect.y = snake[i - 1].rect.y 
        self.rect.x += self.dx
        self.rect.y += self.dy
 

        if self.rect.x > 700:
            self.rect.x = 0
        if self.rect.x < 0:
            self.rect.x = 700
        if self.rect.y < 0:
            self.rect.y = 450
        if self.rect.y > 450:
            self.rect.y = 0
        
    def get_direction(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.dy == 0:
            self.dx = 0
            self.dy = -SQUARE_SIZE
        elif keys[K_DOWN] and self.dy == 0:
            self.dx = 0
            self.dy = SQUARE_SIZE
        elif keys[K_LEFT] and self.dx == 0:
            self.dx = -SQUARE_SIZE
            self.dy = 0
        elif keys[K_RIGHT] and self.dx == 0:
            self.dx = SQUARE_SIZE
            self.dy = 0   

class Apple(GameSprite):
    def __init__(self, pl_image):
        super().__init__(pl_image, 0, 0)
        self.respawn()
    
    def respawn(self):
        self.rect.x = randrange(0, WIDIH - SQUARE_SIZE, SQUARE_SIZE)
        self.rect.y = randrange(0, HEIGHT - SQUARE_SIZE, SQUARE_SIZE)

head = Snake('head.png', 200, 250)
apple = Apple('apple.png')
snake = [head]
clock = time.Clock()
step_time = timer()
running = True
finish = False
while running:

    for e in event.get():
        if e.type == QUIT:
            running = False

    if not finish:
        cur_time = timer()
        W.blit(bg, (0, 0))
        head.get_direction()

        if cur_time - step_time >= 0.5:
            head.update()
            step_time = timer()

            if head.rect.colliderect(apple.rect):
                apple.respawn()
                last_part = snake[-1]
                new_x, new_y = last_part.rect.x, last_part.rect.y 

                if head.dx > 0:
                    new_x += 50
                elif head.dx < 0:
                    new_x += 50
                elif head.dy > 0:
                    new_y -= 50
                elif head.dy < 0:
                    new_y += 50
                
                new_part = Snake('square.png', new_x, new_y)
                snake.append(new_part)

        for part in snake[1:]:
            if head.rect.colliderect(part.rect):
                finish = True
                W.blit(text, (250, 200))


        

        
        head.draw_sprite()
        apple.draw_sprite()

        for part in snake:
            part.draw_sprite()

    display.update()
    clock.tick(FPS)

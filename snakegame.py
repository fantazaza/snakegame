import pygame
import random

WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Snake:
    def __init__(self):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        self.eye_direction = "RIGHT"  # ทิศทางของตา


    def move(self):
        head = self.body[0]
        if self.direction == "UP":
            new_head = (head[0], head[1] - CELL_SIZE)
        elif self.direction == "DOWN":
            new_head = (head[0], head[1] + CELL_SIZE)
        elif self.direction == "LEFT":
            new_head = (head[0] - CELL_SIZE, head[1])
        elif self.direction == "RIGHT":
            new_head = (head[0] + CELL_SIZE, head[1])
        self.body.insert(0, new_head)

    def grow(self):
        tail = self.body[-1]
        if self.direction == "UP":
            new_tail = (tail[0], tail[1] + CELL_SIZE)
        elif self.direction == "DOWN":
            new_tail = (tail[0], tail[1] - CELL_SIZE)
        elif self.direction == "LEFT":
            new_tail = (tail[0] + CELL_SIZE, tail[1])
        elif self.direction == "RIGHT":
            new_tail = (tail[0] - CELL_SIZE, tail[1])
        self.body.append(new_tail)

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
        head = self.body[0]
        eye_offset = CELL_SIZE // 3  # ตำแหน่งของตา
        if self.eye_direction == "UP":
            eye_position = (head[0] + CELL_SIZE // 2, head[1] + eye_offset)
        elif self.eye_direction == "DOWN":
            eye_position = (head[0] + CELL_SIZE // 2, head[1] + CELL_SIZE - eye_offset)
        elif self.eye_direction == "LEFT":
            eye_position = (head[0] + eye_offset, head[1] + CELL_SIZE // 2)
        elif self.eye_direction == "RIGHT":
            eye_position = (head[0] + CELL_SIZE - eye_offset, head[1] + CELL_SIZE // 2)
        pygame.draw.circle(surface, (0,0,0), eye_position, 3)  # วาดตา
        


class Food:
    def __init__(self):
        self.position = (random.randrange(1, WIDTH // CELL_SIZE) * CELL_SIZE,
                         random.randrange(1, HEIGHT // CELL_SIZE) * CELL_SIZE)

    def spawn(self):
        self.position = (random.randrange(1, WIDTH // CELL_SIZE) * CELL_SIZE,
                         random.randrange(1, HEIGHT // CELL_SIZE) * CELL_SIZE)

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

snake = Snake()
food = Food()
game_over = False
exit_game = False
score = 0
SNAKE_COLORS = [(0, 0, 255), (255, 0, 0), (0, 255, 0)]  # สีน้ำเงิน, แดง, เขียว
selected_color_index = 0  # สีของงูที่ถูกเลือก
snake_color = SNAKE_COLORS[selected_color_index]
font = pygame.font.Font(None, 36)
new_game_font = pygame.font.Font(None, 24)

def change_color():
    global selected_color_index, snake_color
    selected_color_index = (selected_color_index + 1) % len(SNAKE_COLORS)  # สลับไปยังสีถัดไปในลิสต์ SNAKE_COLORS
    snake_color = SNAKE_COLORS[selected_color_index]


color_button = pygame.Rect(250, 250, 140, 40)  # ตำแหน่งและขนาดของปุ่มสี
pygame.draw.rect(screen, snake_color, color_button)
color_font = pygame.font.Font(None, 36)
color_text = color_font.render("Change Color", True, WHITE)
screen.blit(color_text, (270, 255))



while not game_over and not exit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != "DOWN":
                snake.direction = "UP"
                snake.eye_direction = "UP"
            elif event.key == pygame.K_DOWN and snake.direction != "UP":
                snake.direction = "DOWN"
                snake.eye_direction = "DOWN"
            elif event.key == pygame.K_LEFT and snake.direction != "RIGHT":
                snake.direction = "LEFT"
                snake.eye_direction = "LEFT"
            elif event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                snake.direction = "RIGHT"
                snake.eye_direction = "RIGHT"
    mouse_pos = pygame.mouse.get_pos()
    if color_button.collidepoint(mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            change_color()
    if not game_over and not exit_game:
        snake.move()
        if snake.body[0] == food.position:
            food.spawn()
            snake.grow()
            score += 1
        else:
            snake.body.pop()  # ไม่ลบส่วนสุดท้ายของงูเมื่อไม่กินผลไม้

        if len(snake.body) > 1 and snake.body[0] in snake.body[1:]:
            game_over = True

        if snake.body[0][0] < 0 or snake.body[0][0] >= WIDTH or snake.body[0][1] < 0 or snake.body[0][1] >= HEIGHT:
            game_over = True

        screen.fill(WHITE)
        snake.draw(screen)
        food.draw(screen)
        score_text = font.render("Score: " + str(score), True, GREEN)
        screen.blit(score_text, (10, 10))
        pygame.display.flip()
        clock.tick(10)

    while game_over and not exit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    snake = Snake()
                    food = Food()
                    game_over = False
                    score = 0
                elif event.key == pygame.K_q:
                    exit_game = True

pygame.quit()

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Player settings
player_size = 50
player_pos = [SCREEN_WIDTH/2, SCREEN_HEIGHT-2*player_size]
player_speed = 10

# Obstacle settings
obstacle_size = 50
obstacle_pos = [random.randint(0, SCREEN_WIDTH-obstacle_size), 0]
obstacle_list = [obstacle_pos]
obstacle_speed = 10

# Score
score = 0

clock = pygame.time.Clock()

# Functions
def set_level(score, obstacle_speed):
    if score < 20:
        obstacle_speed = 5
    elif score < 40:
        obstacle_speed = 8
    elif score < 60:
        obstacle_speed = 12
    else:
        obstacle_speed = 15
    return obstacle_speed

def drop_obstacles(obstacle_list):
    delay = random.random()
    if len(obstacle_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, SCREEN_WIDTH - obstacle_size)
        y_pos = 0
        obstacle_list.append([x_pos, y_pos])

def draw_obstacles(obstacle_list):
    for obstacle_pos in obstacle_list:
        pygame.draw.rect(screen, BLACK, (obstacle_pos[0], obstacle_pos[1], obstacle_size, obstacle_size))

def update_obstacle_positions(obstacle_list, score):
    for idx, obstacle_pos in enumerate(obstacle_list):
        if obstacle_pos[1] >= 0 and obstacle_pos[1] < SCREEN_HEIGHT:
            obstacle_pos[1] += obstacle_speed
        else:
            obstacle_list.pop(idx)
            score += 1
    return score

def collision_check(obstacle_list, player_pos):
    for obstacle_pos in obstacle_list:
        if detect_collision(player_pos, obstacle_pos):
            return True
    return False

def detect_collision(player_pos, obstacle_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    o_x = obstacle_pos[0]
    o_y = obstacle_pos[1]

    if (o_x >= p_x and o_x < (p_x + player_size)) or (p_x >= o_x and p_x < (o_x + obstacle_size)):
        if (o_y >= p_y and o_y < (p_y + player_size)) or (p_y >= o_y and p_y < (o_y + obstacle_size)):
            return True
    return False

# Game Loop
game_over = False
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            x = player_pos[0]
            y = player_pos[1]

            if event.key == pygame.K_LEFT:
                x -= player_size
            elif event.key == pygame.K_RIGHT:
                x += player_size

            player_pos = [x, y]

    screen.fill(WHITE)

    # Update obstacle positions
    drop_obstacles(obstacle_list)
    score = update_obstacle_positions(obstacle_list, score)
    obstacle_speed = set_level(score, obstacle_speed)

    # Draw Obstacles
    draw_obstacles(obstacle_list)

    # Display Player
    pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size, player_size))

    # Collision check
    if collision_check(obstacle_list, player_pos):
        game_over = True
        break

    # Display Score
    font = pygame.font.SysFont(None, 40)
    text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(text, [10, 10])

    clock.tick(30)

    pygame.display.update()

           

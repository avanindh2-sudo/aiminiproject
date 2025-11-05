import pygame
import random
import os

# --- Constants ---
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 30, 30
CELL_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
GRAY = (180, 180, 180)
BG_COLOR = (240, 240, 255)

# --- Pygame Setup ---
pygame.init()
pygame.font.init()
pygame.mixer.init()

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🌟 Maze Game - Player Controlled")
font = pygame.font.SysFont('comicsansms', 36, bold=True)

# --- Load Assets ---
def load_sprite(filename):
    path = os.path.join(os.getcwd(), filename)
    img = pygame.image.load(path)
    return pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE))

player_sprite = load_sprite("player.png")
start_img = load_sprite("start.png")
end_img = load_sprite("end.png")
move_sound = pygame.mixer.Sound("move.wav")
win_sound = pygame.mixer.Sound("win.wav")

# --- Maze Generation (Recursive Backtracking) ---
def generate_maze():
    maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]
    visited = [[False for _ in range(COLS)] for _ in range(ROWS)]

    def carve(x, y):
        visited[x][y] = True
        maze[x][y] = 0
        directions = [(0,1), (1,0), (0,-1), (-1,0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx*2, y + dy*2
            if 0 <= nx < ROWS and 0 <= ny < COLS and not visited[nx][ny]:
                maze[x + dx][y + dy] = 0
                carve(nx, ny)

    carve(0, 0)
    maze[0][0] = 0
    maze[ROWS-1][COLS-1] = 0
    return maze

# --- Drawing ---
def draw_maze(maze, player_pos):
    win.fill(BG_COLOR)
    for i in range(ROWS):
        for j in range(COLS):
            rect = pygame.Rect(j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze[i][j] == 1:
                pygame.draw.rect(win, BLACK, rect)
            else:
                pygame.draw.rect(win, WHITE, rect)
            pygame.draw.rect(win, GRAY, rect, 1)

    win.blit(start_img, (0, 0))
    win.blit(end_img, ((COLS-1)*CELL_SIZE, (ROWS-1)*CELL_SIZE))

    x, y = player_pos
    win.blit(player_sprite, (y*CELL_SIZE, x*CELL_SIZE))
    pygame.display.update()

# --- Text Rendering ---
def draw_text(message, color=(255, 215, 0)):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    win.blit(overlay, (0, 0))

    text_surface = font.render(message, True, color)
    shadow = font.render(message, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    shadow_rect = shadow.get_rect(center=(WIDTH // 2 + 2, HEIGHT // 2 + 2))

    win.blit(shadow, shadow_rect)
    win.blit(text_surface, text_rect)
    pygame.display.update()

# --- Main Game Loop ---
def main():
    maze = generate_maze()
    player_pos = [0, 0]
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)
        draw_maze(maze, player_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        x, y = player_pos

        moved = False
        if keys[pygame.K_UP] and x > 0 and maze[x-1][y] == 0:
            player_pos[0] -= 1
            moved = True
        if keys[pygame.K_DOWN] and x < ROWS-1 and maze[x+1][y] == 0:
            player_pos[0] += 1
            moved = True
        if keys[pygame.K_LEFT] and y > 0 and maze[x][y-1] == 0:
            player_pos[1] -= 1
            moved = True
        if keys[pygame.K_RIGHT] and y < COLS-1 and maze[x][y+1] == 0:
            player_pos[1] += 1
            moved = True

        if moved:
            move_sound.play()

        if player_pos == [ROWS-1, COLS-1]:
            draw_maze(maze, player_pos)
            win_sound.play()
            draw_text("🎉 You Win! Great Job!")
            while pygame.mixer.get_busy():
                pygame.time.Clock().tick(10)
            running = False

main()
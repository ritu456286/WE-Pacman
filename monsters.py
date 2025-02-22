import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 30
WHITE, BLACK, BLUE, YELLOW, RED, PINK, CYAN, ORANGE = (
    (255, 255, 255),
    (0, 0, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 0),
    (255, 192, 203),
    (0, 255, 255),
    (255, 165, 0),
)

# Board Layout (0 = path, 1 = wall, 2 = ghost house)
BOARD = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1, 2, 2, 2, 2, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1, 2, 0, 0, 2, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 2, 0, 0, 2, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

ROWS = len(BOARD)
COLS = len(BOARD[0])

# Pac-Man's starting position
pacman_x, pacman_y = 1, 1
pacman_dir = (0, 1)  # Default moving right

# Ghost class
class Ghost:
    def __init__(self, x, y, color, strategy):
        self.x, self.y = x, y
        self.color = color
        self.strategy = strategy  # Determines behavior

    def move(self):
        possible_moves = [
            (self.x - 1, self.y), (self.x + 1, self.y),  # Up, Down
            (self.x, self.y - 1), (self.x, self.y + 1)   # Left, Right
        ]
        valid_moves = [(nx, ny) for nx, ny in possible_moves if can_move(nx, ny)]

        if not valid_moves:
            return  # No movement possible

        if self.strategy == "chase":  # Blinky
            target = (pacman_x, pacman_y)  # Always chase Pac-Man's current position

        elif self.strategy == "ambush":  # Pinky
            target = (pacman_x + 4 * pacman_dir[0], pacman_y + 4 * pacman_dir[1])
            # Ensure target is within bounds
            target = (max(0, min(ROWS - 1, target[0])), max(0, min(COLS - 1, target[1])))

        elif self.strategy == "unpredictable":  # Inky
            blinky_x, blinky_y = ghosts[0].x, ghosts[0].y  # Get Blinky’s position
            mid_x = pacman_x + (pacman_x - blinky_x) * 2
            mid_y = pacman_y + (pacman_y - blinky_y) * 2
            target = (mid_x, mid_y)
            # Ensure target is within bounds
            target = (max(0, min(ROWS - 1, target[0])), max(0, min(COLS - 1, target[1])))

        elif self.strategy == "scatter":  # Clyde
            if distance((self.x, self.y), (pacman_x, pacman_y)) > 8:
                target = (pacman_x, pacman_y)
            else:
                target = (ROWS - 2, 0)  # Bottom-left corner

        # Move towards the target
        self.x, self.y = min(valid_moves, key=lambda pos: distance(pos, target))

# Initialize ghosts
ghosts = [
    Ghost(4, 9, RED, "chase"),  # Blinky
    Ghost(4, 10, PINK, "ambush"),  # Pinky
    Ghost(5, 9, CYAN, "unpredictable"),  # Inky
    Ghost(5, 10, ORANGE, "scatter"),  # Clyde
]

# Function to draw the board
def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            x, y = col * GRID_SIZE, row * GRID_SIZE
            if BOARD[row][col] == 1:
                pygame.draw.rect(screen, BLUE, (x, y, GRID_SIZE, GRID_SIZE))
            elif BOARD[row][col] == 2:
                pygame.draw.rect(screen, WHITE, (x, y, GRID_SIZE, GRID_SIZE))
            else:
                pygame.draw.rect(screen, BLACK, (x, y, GRID_SIZE, GRID_SIZE))

# Function to draw Pac-Man
def draw_pacman():
    x, y = pacman_y * GRID_SIZE + GRID_SIZE // 2, pacman_x * GRID_SIZE + GRID_SIZE // 2
    pygame.draw.circle(screen, YELLOW, (x, y), GRID_SIZE // 2 - 2)

# Function to draw ghosts
def draw_ghosts():
    for ghost in ghosts:
        x, y = ghost.y * GRID_SIZE + GRID_SIZE // 2, ghost.x * GRID_SIZE + GRID_SIZE // 2
        pygame.draw.circle(screen, ghost.color, (x, y), GRID_SIZE // 2 - 2)

# Function to check if movement is allowed
def can_move(x, y):
    return 0 <= x < ROWS and 0 <= y < COLS and BOARD[x][y] != 1

# Function to calculate distance (Manhattan)
def distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# Function to check if Pac-Man is caught
def check_collision():
    global running
    for ghost in ghosts:
        if ghost.x == pacman_x and ghost.y == pacman_y:
            return True
    return False

# Game loop
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man with Monsters")

running = True
game_over = False

while running:
    screen.fill(BLACK)
    draw_board()
    
    if game_over:
        font = pygame.font.Font(None, 50)
        text = font.render("Game Over! Press R to Restart", True, WHITE)
        screen.blit(text, (100, HEIGHT // 2))
    else:
        draw_pacman()
        draw_ghosts()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_r:
                    pacman_x, pacman_y = 1, 1
                    game_over = False
                if event.key == pygame.K_UP and can_move(pacman_x - 1, pacman_y): pacman_x -= 1
                if event.key == pygame.K_DOWN and can_move(pacman_x + 1, pacman_y): pacman_x += 1
                if event.key == pygame.K_LEFT and can_move(pacman_x, pacman_y - 1): pacman_y -= 1
                if event.key == pygame.K_RIGHT and can_move(pacman_x, pacman_y + 1): pacman_y += 1

        for ghost in ghosts:
            ghost.move()

        if check_collision():
            game_over = True

    pygame.display.flip()
    pygame.time.delay(200)

pygame.quit()

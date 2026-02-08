import sys
import pygame
import numpy as np

pygame.init()

#  COLORS 
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

#  DIMENSIONS 
WIDTH = 300
HEIGHT = 300
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 20

#  SCREEN 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe AI")
screen.fill(BLACK)

#  BOARD 
board = np.zeros((BOARD_ROWS, BOARD_COLS))


#  FUNCTIONS 
def draw_lines():
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, WHITE, (0, i * SQUARE_SIZE),
                         (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, WHITE, (i * SQUARE_SIZE, 0),
                         (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)


def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(
                    screen, WHITE,
                    (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                     row * SQUARE_SIZE + SQUARE_SIZE // 2),
                    CIRCLE_RADIUS, CIRCLE_WIDTH
                )
            elif board[row][col] == 2:
                pygame.draw.line(
                    screen, WHITE,
                    (col * SQUARE_SIZE + SQUARE_SIZE // 4,
                     row * SQUARE_SIZE + SQUARE_SIZE // 4),
                    (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4,
                     row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4),
                    CROSS_WIDTH
                )
                pygame.draw.line(
                    screen, WHITE,
                    (col * SQUARE_SIZE + SQUARE_SIZE // 4,
                     row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4),
                    (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4,
                     row * SQUARE_SIZE + SQUARE_SIZE // 4),
                    CROSS_WIDTH
                )


def mark_square(row, col, player):
    board[row][col] = player


def available_square(row, col):
    return board[row][col] == 0


def is_board_full(b):
    return not np.any(b == 0)


def check_win(player, b=board):
    for i in range(3):
        if all(b[i, :] == player) or all(b[:, i] == player):
            return True
    if b[0][0] == b[1][1] == b[2][2] == player:
        return True
    if b[2][0] == b[1][1] == b[0][2] == player:
        return True
    return False


def minimax(b, is_max):
    if check_win(2, b):
        return 1
    if check_win(1, b):
        return -1
    if is_board_full(b):
        return 0

    if is_max:
        best = -1000
        for r in range(3):
            for c in range(3):
                if b[r][c] == 0:
                    b[r][c] = 2
                    best = max(best, minimax(b, False))
                    b[r][c] = 0
        return best
    else:
        best = 1000
        for r in range(3):
            for c in range(3):
                if b[r][c] == 0:
                    b[r][c] = 1
                    best = min(best, minimax(b, True))
                    b[r][c] = 0
        return best


def best_move():
    best_score = -1000
    move = (-1, -1)

    for r in range(3):
        for c in range(3):
            if board[r][c] == 0:
                board[r][c] = 2
                score = minimax(board, False)
                board[r][c] = 0

                if score > best_score:
                    best_score = score
                    move = (r, c)

    mark_square(move[0], move[1], 2)


def show_text(text, color):
    font = pygame.font.SysFont(None, 40)
    label = font.render(text, True, color)
    rect = label.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(label, rect)


# ================= MAIN =================
draw_lines()
game_over = False
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = event.pos
            row = y // SQUARE_SIZE
            col = x // SQUARE_SIZE

            if available_square(row, col):
                mark_square(row, col, 1)

                if check_win(1):
                    game_over = True
                elif not is_board_full(board):
                    best_move()
                    if check_win(2):
                        game_over = True
                else:
                    game_over = True

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            board[:] = 0
            screen.fill(BLACK)
            draw_lines()
            game_over = False

    draw_figures()

    if game_over:
        if check_win(1):
            show_text("You Win!", GREEN)
        elif check_win(2):
            show_text("AI Wins!", RED)
        else:
            show_text("It's a Draw!", GRAY)

    pygame.display.update()

pygame.quit()
sys.exit()

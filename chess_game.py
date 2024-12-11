import pygame
import os
import random  # For AI moves

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800  # Increased width for sidebars
SIDEBAR_WIDTH = 200  # Width for each sidebar
BOARD_WIDTH = SCREEN_WIDTH - 2 * SIDEBAR_WIDTH  # Central board area
ROWS, COLS = 8, 8
SQUARE_SIZE = BOARD_WIDTH // COLS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 40)

# Load images
PIECES = {}
for piece in ["wp", "bp", "wr", "br", "wn", "bn", "wb", "bb", "wq", "bq", "wk", "bk"]:
    PIECES[piece] = pygame.image.load(os.path.join("assets", f"{piece}.png"))

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess Game")

# Piece names
PIECE_NAMES = {
    "wp": "White Pawn", "bp": "Black Pawn",
    "wr": "White Rook", "br": "Black Rook",
    "wn": "White Knight", "bn": "Black Knight",
    "wb": "White Bishop", "bb": "Black Bishop",
    "wq": "White Queen", "bq": "Black Queen",
    "wk": "White King", "bk": "Black King",
}


def draw_text(text, x, y, color=WHITE):
    """Draw text on the screen."""
    label = FONT.render(text, True, color)
    screen.blit(label, (x, y))


def initialize_board():
    """Initialize the chess board."""
    return [
        ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
        ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
        ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]
    ]


def draw_board():
    """Draw the chess board."""
    colors = [WHITE, BLACK]
    for row in range(ROWS):
        for col in range(COLS):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, (SIDEBAR_WIDTH + col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_pieces(board):
    """Draw the chess pieces."""
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != "--":
                x = SIDEBAR_WIDTH + col * SQUARE_SIZE
                y = row * SQUARE_SIZE
                screen.blit(pygame.transform.scale(PIECES[piece], (SQUARE_SIZE, SQUARE_SIZE)), (x, y))


def get_valid_moves(board, piece, row, col):
    """Get valid moves for a piece."""
    moves = []
    directions = {
        "p": [(-1, 0), (-2, 0), (-1, -1), (-1, 1)],  # Pawn moves
        "r": [(1, 0), (-1, 0), (0, 1), (0, -1)],  # Rook moves
        "b": [(1, 1), (1, -1), (-1, 1), (-1, -1)],  # Bishop moves
        "q": [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)],  # Queen moves
        "k": [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)],  # King moves
        "n": [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)]  # Knight moves
    }

    if piece[1] == "p":  # Pawn-specific logic
        direction = -1 if piece[0] == "w" else 1
        start_row = 6 if piece[0] == "w" else 1
        if board[row + direction][col] == "--":
            moves.append((row + direction, col))
            if row == start_row and board[row + 2 * direction][col] == "--":
                moves.append((row + 2 * direction, col))
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            r, c = row + dr * direction, col + dc
            if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] != "--" and board[r][c][0] != piece[0]:
                moves.append((r, c))
    else:  # For other pieces
        for dr, dc in directions[piece[1]]:
            r, c = row + dr, col + dc
            while 0 <= r < ROWS and 0 <= c < COLS:
                if board[r][c] == "--":
                    moves.append((r, c))
                elif board[r][c][0] != piece[0]:
                    moves.append((r, c))
                    break
                else:
                    break
                if piece[1] in ["k", "n"]:  # King and Knight do not slide
                    break
                r, c = r + dr, c + dc

    return moves


def display_captured_pieces(captured_pieces, title, x, y):
    """Display captured pieces in the sidebar."""
    pygame.draw.rect(screen, BLACK, (x, y, SIDEBAR_WIDTH - 10, SCREEN_HEIGHT - 10))  # Sidebar background
    draw_text(title, x + 10, y + 10, WHITE)
    for i, piece in enumerate(captured_pieces):
        piece_name = PIECE_NAMES.get(piece, "Unknown")
        draw_text(piece_name, x + 10, y + 40 + i * 20, WHITE)


def get_random_move(board, color):
    """Generate a random valid move for the AI."""
    all_moves = []
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != "--" and piece[0] == color:
                moves = get_valid_moves(board, piece, row, col)
                for move in moves:
                    all_moves.append((row, col, move))
    return random.choice(all_moves) if all_moves else None


def display_game_over_screen(message):
    """Display the game over screen."""
    screen.fill(BLACK)
    draw_text(message, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, WHITE)
    draw_text("Press any key to exit", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50, WHITE)
    pygame.display.flip()

    # Wait for a key press to exit
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN:
                waiting = False


def check_game_over(board, captured_by_player, captured_by_ai):
    """Check if the game is over."""
    for captured in captured_by_player:
        if captured == "bk":  # Player captures black king
            display_game_over_screen("You Win!")
            return True
    for captured in captured_by_ai:
        if captured == "wk":  # AI captures white king
            display_game_over_screen("You Lose!")
            return True
    return False


def choose_side():
    """Display a menu for the player to choose their side."""
    choosing = True
    choice = None

    while choosing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:  # Choose White
                    choice = "w"
                    choosing = False
                elif event.key == pygame.K_b:  # Choose Black
                    choice = "b"
                    choosing = False

        screen.fill(BLACK)
        draw_text("Choose Your Side", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100, WHITE)
        draw_text("Press W for White", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, WHITE)
        draw_text("Press B for Black", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50, WHITE)
        pygame.display.flip()

    return choice


def two_player_with_ai(player_side):
    """Start a game with player choice of side."""
    clock = pygame.time.Clock()
    running = True
    board = initialize_board()
    selected_piece = None
    selected_pos = None
    valid_moves = []
    turn = "w"  # White always starts
    captured_by_player = []  # Pieces captured by the player
    captured_by_ai = []  # Pieces captured by the AI

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if turn == player_side and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col, row = (x - SIDEBAR_WIDTH) // SQUARE_SIZE, y // SQUARE_SIZE
                if col < 0 or col >= COLS or row >= ROWS:  # Ignore clicks outside the board
                    continue

                if selected_piece:
                    if (row, col) in valid_moves:
                        if board[row][col] != "--":  # Capturing a piece
                            captured_by_player.append(board[row][col])
                        board[row][col] = selected_piece
                        board[selected_pos[1]][selected_pos[0]] = "--"
                        turn = "b" if player_side == "w" else "w"  # Switch to AI
                    selected_piece = None
                    valid_moves = []
                else:
                    piece = board[row][col]
                    if piece != "--" and piece[0] == turn:
                        selected_piece = piece
                        selected_pos = (col, row)
                        valid_moves = get_valid_moves(board, piece, row, col)

        # AI's turn
        if turn != player_side:
            ai_move = get_random_move(board, "b" if player_side == "w" else "w")
            if ai_move:
                start_row, start_col, (end_row, end_col) = ai_move
                if board[end_row][end_col] != "--":  # Capturing a piece
                    captured_by_ai.append(board[end_row][end_col])
                board[end_row][end_col] = board[start_row][start_col]
                board[start_row][start_col] = "--"
                turn = player_side  # Switch back to player

        # Check if the game is over
        if check_game_over(board, captured_by_player, captured_by_ai):
            running = False

        # Draw the game
        screen.fill(BLACK)  # Clear the screen
        display_captured_pieces(captured_by_player, "Your Captures", 10, 10)
        display_captured_pieces(captured_by_ai, "AI Captures", SCREEN_WIDTH - SIDEBAR_WIDTH + 10, 10)
        draw_board()
        draw_pieces(board)
        for move in valid_moves:
            pygame.draw.circle(screen, (0, 255, 0), (SIDEBAR_WIDTH + move[1] * SQUARE_SIZE + SQUARE_SIZE // 2, move[0] * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


def display_tutorial():
    """Display the tutorial screen."""
    tutorial_running = True
    steps = [
        "Welcome to Chess Tutorial!",
        "You are on the white side. Win the black team!",
        "Step 1: Learn the board and pieces.",
        "Step 2: Pawns can move forward one square.",
        "Step 3: Rooks move horizontally or vertically.",
        "Step 4: Knights move in an L-shape.",
        "Step 5: Bishops move diagonally.",
        "Step 6: The Queen moves any number of squares in any direction.",
        "Step 7: The King moves one square in any direction.",
        "Press any key to return to the main menu."
    ]

    while tutorial_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:  # Exit tutorial on key press
                tutorial_running = False

        screen.fill(BLACK)
        y_offset = 50
        for step in steps:
            draw_text(step, 50, y_offset, WHITE)
            y_offset += 40
        pygame.display.flip()


def main():
    """Main function to start the game."""
    running = True
    while running:
        screen.fill(BLACK)
        draw_text("Chess Game", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, WHITE)
        draw_text("1. Start Game", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, WHITE)
        draw_text("2. Tutorial", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, WHITE)
        draw_text("Press Q to quit", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, WHITE)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Start game
                    player_side = choose_side()  # Get player's side
                    two_player_with_ai(player_side)
                elif event.key == pygame.K_2:  # Open tutorial
                    display_tutorial()
                elif event.key == pygame.K_q:  # Quit
                    running = False

    pygame.quit()


if __name__ == "__main__":
    main()

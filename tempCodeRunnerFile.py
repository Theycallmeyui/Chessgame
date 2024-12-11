import pygame
import sys
from chess_game import main as start_chess_game  # Import the chess game's main function

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 60)
BUTTON_FONT = pygame.font.Font(None, 40)
TEXT_FONT = pygame.font.Font(None, 30)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess Game Menu")


def draw_text(text, x, y, font=FONT, color=WHITE):
    """Draw text on the screen."""
    label = font.render(text, True, color)
    screen.blit(label, (x, y))


def draw_button(text, x, y, width, height, action=None):
    """Draw a button and handle clicks."""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, (100, 100, 100), (x, y, width, height))  # Hover effect
        if click[0] == 1 and action is not None:
            pygame.time.wait(300)  # Avoid multiple clicks
            action()
    else:
        pygame.draw.rect(screen, (50, 50, 50), (x, y, width, height))

    text_surface = BUTTON_FONT.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)


def show_tutorial():
    """Show the tutorial screen."""
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        draw_text("Tutorial", SCREEN_WIDTH // 2 - 100, 20)

        # Instructions for gameplay
        draw_text("1. Click on a piece to select it.", 50, 100, TEXT_FONT)
        draw_text("2. Green circles show valid moves.", 50, 140, TEXT_FONT)
        draw_text("3. Capture the enemy king to win.", 50, 180, TEXT_FONT)

        # Chess pieces explanation
        draw_text("Chess Pieces:", 50, 240, TEXT_FONT)
        draw_text("Pawn: Moves forward 1 square, captures diagonally.", 50, 280, TEXT_FONT)
        draw_text("Rook: Moves in straight lines (horizontally/vertically).", 50, 320, TEXT_FONT)
        draw_text("Knight: Moves in 'L' shape (2+1 or 1+2).", 50, 360, TEXT_FONT)
        draw_text("Bishop: Moves diagonally any number of squares.", 50, 400, TEXT_FONT)
        draw_text("Queen: Moves in straight or diagonal lines.", 50, 440, TEXT_FONT)
        draw_text("King: Moves 1 square in any direction.", 50, 480, TEXT_FONT)

        # Back button
        draw_button("Back", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 80, 200, 50, main_menu)

        pygame.display.flip()


def main_menu():
    """Display the main menu."""
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        draw_text("Chess Game", SCREEN_WIDTH // 2 - 150, 50)

        draw_button("Start Game", SCREEN_WIDTH // 2 - 100, 200, 200, 50, start_chess_game)
        draw_button("Tutorial", SCREEN_WIDTH // 2 - 100, 300, 200, 50, show_tutorial)
        draw_button("Exit", SCREEN_WIDTH // 2 - 100, 400, 200, 50, sys.exit)

        pygame.display.flip()


if __name__ == "__main__":
    main_menu()

import pygame
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
FONT = pygame.font.SysFont("comicsans", 60)
ATTEMPT_FONT = pygame.font.SysFont("comicsans", 40)
MAX_ATTEMPTS = 3

# Screen Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Word Puzzle Game")

# Background Setup
try:
    background_image = pygame.image.load("background.png").convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
except pygame.error:
    background_image = None

class WordPuzzle:
    def __init__(self, word):
        self.word = word.upper()
        self.scrambled_word = ''.join(random.sample(self.word, len(self.word)))
        self.guess = ""
        self.win = False
        self.attempts = 0
        self.game_over = False

    def draw(self):
        screen.fill(WHITE)  # Clear the screen
        if background_image:
            screen.blit(background_image, (0, 0))
        
        if not self.game_over:
            scrambled_text = FONT.render(f"Scrambled: {self.scrambled_word}", True, BLACK)
            guess_text = FONT.render(f"Your Guess: {self.guess}", True, BLACK)
            attempts_text = ATTEMPT_FONT.render(f"Attempts: {self.attempts}/{MAX_ATTEMPTS}", True, RED)
            screen.blit(scrambled_text, (WIDTH // 2 - scrambled_text.get_width() // 2, HEIGHT // 3))
            screen.blit(guess_text, (WIDTH // 2 - guess_text.get_width() // 2, HEIGHT // 2))
            screen.blit(attempts_text, (WIDTH // 2 - attempts_text.get_width() // 2, HEIGHT // 5))
            
            if self.win:
                win_text = FONT.render("You Win!", True, GREEN)
                screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 + 100))
        else:
            game_over_text = FONT.render("Game Over!", True, RED)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

    def submit_guess(self):
        if self.guess == self.word:
            self.win = True
        else:
            self.attempts += 1
            if self.attempts >= MAX_ATTEMPTS:
                self.game_over = True
        self.guess = ""

    def update_guess(self, char):
        if char == "BACKSPACE":
            self.guess = self.guess[:-1]
        elif len(self.guess) < len(self.word):
            self.guess += char.upper()

# Game Initialization
words = ["PYTHON", "DEVELOPER", "PUZZLE", "COMPUTER", "PROGRAM"]
selected_word = random.choice(words)
puzzle = WordPuzzle(selected_word)
running = True

# Game Loop
while running:
    puzzle.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not puzzle.win and not puzzle.game_over:
            if event.key == pygame.K_BACKSPACE:
                puzzle.update_guess("BACKSPACE")
            elif event.key == pygame.K_RETURN:
                puzzle.submit_guess()
            else:
                puzzle.update_guess(event.unicode)
        elif event.type == pygame.KEYDOWN and (puzzle.win or puzzle.game_over):
            if event.key == pygame.K_RETURN:
                selected_word = random.choice(words)
                puzzle = WordPuzzle(selected_word)

pygame.quit()

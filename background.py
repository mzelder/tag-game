import pygame

BACKGROUND_COLOR = "#07071a"
GRID_COLOR = "#16163d"
GRID_ACCENT_COLOR = "#26265e"
GRID_SIZE = 50

def make_background(screen_width: int, screen_height: int) -> pygame.Surface:
    background = pygame.Surface((screen_width, screen_height))
    background.fill(BACKGROUND_COLOR)
    for x in range(0, screen_width, GRID_SIZE):
        color = GRID_ACCENT_COLOR if x % (GRID_SIZE * 5) == 0 else GRID_COLOR
        pygame.draw.line(background, color, (x, 0), (x, screen_height))
    for y in range(0, screen_height, GRID_SIZE):
        color = GRID_ACCENT_COLOR if y % (GRID_SIZE * 5) == 0 else GRID_COLOR
        pygame.draw.line(background, color, (0, y), (screen_width, y))
    return background
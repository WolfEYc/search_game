import pygame

UI_HEIGHT = 100  # in pixels
SCREEN_WIDTH = 800  # in pixels
SCREEN_HEIGHT = SCREEN_WIDTH + UI_HEIGHT  # in pixels
COLORS = 4  # RGBA
ANTI_ALIAS_TEXT = True
PATH_PAINTBRUSH_SIZE = 20  # in pixels

DEFAULT_FONT_COLOR = pygame.Color(255, 255, 255)
DEFAULT_FONT_SIZE = 36
DEFAULT_FONT_FILE = None

UI_GRID_SCALE = 20  # in pixels
GRID_SCALE = 10  # in pixels
GRID_HEIGHT = SCREEN_WIDTH // GRID_SCALE  # in grid units
GRID_WIDTH = SCREEN_WIDTH // GRID_SCALE  # in grid units

GRID_TOP = UI_HEIGHT
GRID_LEFT = 0
GLOW_SCALE = 1.5
GLOW_STARTING_SIZE = GRID_SCALE * GLOW_SCALE
GLOW_FADE_DURATION = 0.5  # in seconds
GLOW_EXPONENT = 3
GLOW_COLOR = pygame.Color(255, 0, 128)

print(f"{GRID_SCALE=}")
print(f"{GRID_HEIGHT=}")
print(f"{GRID_WIDTH=}")

WALL_COLOR = pygame.Color(0, 0, 0, 0)
PATH_COLOR = pygame.Color(255, 255, 255)
START_COLOR = pygame.Color(0, 255, 0)
END_COLOR = pygame.Color(255, 0, 0)
WALKED_COLOR = pygame.Color(0, 0, 255)
VISITED_COLOR = pygame.Color(255, 255, 0, 128)
ARROW_COLOR = pygame.Color(255, 0, 0)

DEFAULT_COLOR_PALLETTE = [PATH_COLOR, START_COLOR, END_COLOR]

default_font: pygame.font.Font

CLOCK = pygame.time.Clock()
INITIAL_WINDOW_CAPTION = "Pathfinding"
DEFAULT_FPS = 60

PATHFIND_TICK = 0.05  # in seconds


def init():
    global default_font
    default_font = pygame.font.Font(DEFAULT_FONT_FILE, DEFAULT_FONT_SIZE)


def render_text(text: str):
    return default_font.render(text, ANTI_ALIAS_TEXT, DEFAULT_FONT_COLOR)


def glow_sample_curve(glow_pct: float):
    return glow_pct**GLOW_EXPONENT

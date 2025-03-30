import pygame


class Config:
    GRAVITY = 0.75
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
    ANIMATION_COOLDOWN = 100
    ROWS = 16
    COLS = 150
    TILE_SIZE = SCREEN_HEIGHT // ROWS
    TILE_TYPE = 21
    MAXS_LEVELS = 3
    level = 1
    EXPLOSION_SPEED = 4
    screen_scroll = 0
    bg_scroll = 0
    SCROLL_THRESH = 200
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    bullet_group = pygame.sprite.Group()
    grenade_group = pygame.sprite.Group()
    explosion_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    item_box_group = pygame.sprite.Group()
    decoration_group = pygame.sprite.Group()
    water_group = pygame.sprite.Group()
    exit_group = pygame.sprite.Group()

    @staticmethod
    def get_font():
        """Ensure the font is initialized correctly."""
        return pygame.font.SysFont('Futura', 30)

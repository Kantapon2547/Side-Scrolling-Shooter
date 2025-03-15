import pygame


class Config:
    GRAVITY = 0.75
    SCREEN_WIDTH = 800
    ANIMATION_COOLDOWN = 100
    TILE_SIZE = 50
    EXPLOSION_SPEED = 4
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

    bullet_group = pygame.sprite.Group()
    grenade_group = pygame.sprite.Group()
    explosion_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    item_box_group = pygame.sprite.Group()

    @staticmethod
    def get_font():
        """Ensure the font is initialized correctly."""
        return pygame.font.SysFont('Futura', 30)

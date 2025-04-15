import pygame

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()


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
    PINK = (235, 65, 54)

    bullet_group = pygame.sprite.Group()
    grenade_group = pygame.sprite.Group()
    explosion_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    item_box_group = pygame.sprite.Group()
    decoration_group = pygame.sprite.Group()
    water_group = pygame.sprite.Group()
    exit_group = pygame.sprite.Group()

    # load music and sounds
    pygame.mixer.music.load('audio/music2.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1, 0.0, 5000)
    jump_fx = pygame.mixer.Sound('audio/jump.wav')
    jump_fx.set_volume(0.5)
    shot_fx = pygame.mixer.Sound('audio/shot.wav')
    shot_fx.set_volume(0.5)
    grenade_fx = pygame.mixer.Sound('audio/grenade.wav')
    grenade_fx.set_volume(0.5)

    @staticmethod
    def get_font():
        """Ensure the font is initialized correctly."""
        return pygame.font.SysFont('Futura', 30)

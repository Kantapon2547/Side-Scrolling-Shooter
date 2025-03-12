import pygame


class Config:
    GRAVITY = 0.75
    SCREEN_WIDTH = 800
    ANIMATION_COOLDOWN = 100
    SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
    bullet_group = pygame.sprite.Group()
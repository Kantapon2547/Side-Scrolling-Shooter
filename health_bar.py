import pygame
from game_config import Config


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, x, y, health, max_health):
        super().__init__()
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health, screen):
        self.health = health

        ratio = self.health / self.max_health
        pygame.draw.rect(screen, Config.BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, Config.RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, Config.GREEN, (self.x, self.y, 150 * ratio, 20))


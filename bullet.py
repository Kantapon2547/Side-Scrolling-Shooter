import pygame
from game_config import Config


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.speed = 10
        self.image = pygame.image.load('img/icons/bullet.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self, player, enemy, world):
        self.rect.x += (self.direction * self.speed) + Config.screen_scroll

        # Check if bullet it goes off-screen
        if self.rect.right < 0 or self.rect.left > Config.SCREEN_WIDTH:
            self.kill()
        # Check for collision with level
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()
        # Check for collision with player or enemy
        if pygame.sprite.spritecollide(player, Config.bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        for enemy in Config.enemy_group:
            if pygame.sprite.spritecollide(enemy, Config.bullet_group, False):
                if enemy.alive:
                    enemy.health -= 25
                    self.kill()

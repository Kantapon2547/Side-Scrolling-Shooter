import pygame.sprite
from game_config import Config


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, player):
        super().__init__()
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.image = pygame.image.load('img/icons/grenade.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.player = player

    def update(self):
        self.vel_y += Config.GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y

        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.speed = 0

        if self.rect.left + dx < 0 or self.rect.right + dx > Config.SCREEN_WIDTH:
            self.direction *= -1
            dx = self.direction * self.speed

        self.rect.x += dx
        self.rect.y += dy

        # countdown timer
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y, 0.5)
            Config.explosion_group.add(explosion)
            # do damage to anyone that is nearby
            if abs(self.rect.centerx - self.player.rect.centerx) < Config.TILE_SIZE * 2 and \
                    abs(self.rect.centery - self.player.rect.centery) < Config.TILE_SIZE * 2:
                self.player.health -= 50
            for enemy in Config.enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < Config.TILE_SIZE * 2 and \
                     abs(self.rect.centery - enemy.rect.centery) < Config.TILE_SIZE * 2:
                    enemy.health -= 50


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        super().__init__()
        self.scale = scale
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f'img/explosion/exp{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # update explosion animation
        self.counter += 1

        if self.counter >= Config.EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            # if animation is complete then delete the explosion
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]

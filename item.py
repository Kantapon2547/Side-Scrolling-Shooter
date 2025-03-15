import pygame
from game_config import Config

pygame.init()
pygame.display.set_mode((1, 1))

health_box_img = pygame.image.load(f'img/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load(f'img/icons/ammo_box.png').convert_alpha()
grenade_box_img = pygame.image.load(f'img/icons/grenade_box.png').convert_alpha()
item_boxes = {
    'Health': health_box_img,
    'Ammo': ammo_box_img,
    'Grenade': grenade_box_img
}


class Item(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        super().__init__()
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + Config.TILE_SIZE // 2, y + (Config.TILE_SIZE - self.image.get_height()))

    def update(self, player):
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == 'Health':
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Ammo':
                player.ammo += 15
            elif self.item_type == 'Grenade':
                player.grenades += 3

            self.kill()

import pygame
from character import Soldier
from item import Item
from game_config import Config
from health_bar import HealthBar

# Store tiles in a list and load images
img_list = []
for tile_index in range(Config.TILE_TYPE):
    tile_img = pygame.image.load(f'img/Tile/{tile_index}.png')
    tile_img = pygame.transform.scale(tile_img, (Config.TILE_SIZE, Config.TILE_SIZE))
    img_list.append(tile_img)


    class Decoration(pygame.sprite.Sprite):
        def __init__(self, img, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.midtop = (x + Config.TILE_SIZE // 2, y + (Config.TILE_SIZE - self.image.get_height()))

    class Water(pygame.sprite.Sprite):
        def __init__(self, img, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.midtop = (x + Config.TILE_SIZE // 2, y + (Config.TILE_SIZE - self.image.get_height()))

    class Exit(pygame.sprite.Sprite):
        def __init__(self, img, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.midtop = (x + Config.TILE_SIZE // 2, y + (Config.TILE_SIZE - self.image.get_height()))


class World:
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * Config.TILE_SIZE
                    img_rect.y = y * Config.TILE_SIZE
                    tile_data = (img, img_rect)
                    if 0 <= tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 9 and tile <= 10:
                        water = Water(img, x * Config.TILE_SIZE, y * Config.TILE_SIZE)
                        Config.water_group.add(water)
                    elif tile >= 11 and tile <= 14:
                        decoration = Decoration(img, x * Config.TILE_SIZE, y * Config.TILE_SIZE)
                        Config.decoration_group.add(decoration)
                    elif tile == 15:  # create player
                        player = Soldier('player', x * Config.TILE_SIZE, y * Config.TILE_SIZE, 1.65, 5, 20, 5)
                        health_bar = HealthBar(10, 10, player.health, player.health)
                    elif tile == 16:  # create enemies
                        enemy = Soldier('enemy', x * Config.TILE_SIZE, y * Config.TILE_SIZE, 1.65, 2, 20, 0)
                        Config.enemy_group.add(enemy)
                    elif tile == 17:  # create ammo box
                        item_box = Item('Ammo', x * Config.TILE_SIZE, y * Config.TILE_SIZE)
                        Config.item_box_group.add(item_box)
                    elif tile == 18:  # create grenade box
                        item_box = Item('Grenade', x * Config.TILE_SIZE, y * Config.TILE_SIZE)
                        Config.item_box_group.add(item_box)
                    elif tile == 19:  # create health box
                        item_box = Item('Health', x * Config.TILE_SIZE, y * Config.TILE_SIZE)
                        Config.item_box_group.add(item_box)
                    elif tile == 20:  # create exit
                        exit = Exit(img, x * Config.TILE_SIZE, y * Config.TILE_SIZE)
                        Config.exit_group.add(exit)

        return player, health_bar  # Move the return outside of the loop

    def draw(self, screen):
        for tile in self.obstacle_list:
            screen.blit(tile[0], tile[1])

import pygame
from game_config import Config
from character import Soldier
from grenades import Grenade
from world import World
import csv
import button


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        pygame.display.set_caption("Shooter")
        self.running = True
        self.moving_left = False
        self.moving_right = False
        self.shoot = False
        self.grenade = False
        self.grenade_thrown = False
        self.start_game = False
        self.bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
        self.grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()
        # load images
        self.pine1_img = pygame.image.load('img/Background/pine1.png').convert_alpha()
        self.pine2_img = pygame.image.load('img/Background/pine2.png').convert_alpha()
        self.mountain_img = pygame.image.load('img/Background/mountain.png').convert_alpha()
        self.sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()

        self.clock = pygame.time.Clock()
        self.FPS = 60

        # button images
        self.start_img = pygame.image.load('img/start_btn.png').convert_alpha()
        self.exit_img = pygame.image.load('img/exit_btn.png').convert_alpha()
        self.restart_img = pygame.image.load('img/restart_btn.png').convert_alpha()

        self.BG = (144, 201, 120)
        # self.BG = (255, 253, 208)

        # create button
        self.start_button = button.Button(Config.SCREEN_WIDTH // 2 - 130, Config.SCREEN_HEIGHT // 2 - 150,
                                          self.start_img, 1)
        self.exit_button = button.Button(Config.SCREEN_WIDTH // 2 - 110, Config.SCREEN_HEIGHT // 2 + 50,
                                         self.exit_img, 1)
        self.restart_button = button.Button(Config.SCREEN_WIDTH // 2 - 100, Config.SCREEN_HEIGHT // 2 - 50,
                                            self.restart_img, 2)

        self.bullet_group = Config.bullet_group
        self.grenade_group = Config.grenade_group
        self.explosion_group = Config.explosion_group
        self.enemy_group = Config.enemy_group
        self.item_box_group = Config.item_box_group
        self.decoration_group = Config.decoration_group
        self.water_group = Config.water_group
        self.exit_group = Config.exit_group

        self.enemy = Soldier('enemy', 400, 200, 1.65, 2, 20, 0)

        # create empty tile list
        world_data = []
        for row in range(Config.ROWS):
            r = [-1] * Config.COLS
            world_data.append(r)
        # load in level data and create world
        with open(f'level_{Config.level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)

        self.world = World()
        self.player, self.health_bar = self.world.process_data(world_data)

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def draw_bg(self):
        self.screen.fill(self.BG)
        # pygame.draw.line(self.screen, Config.RED, (0, 300), (Config.SCREEN_WIDTH, 300))
        width = self.sky_img.get_width()
        for x in range(5):
            self.screen.blit(self.sky_img, ((x * width) - Config.bg_scroll * 0.5, 0))
            self.screen.blit(self.mountain_img, ((x * width) - Config.bg_scroll * 0.6,
                                                 Config.SCREEN_HEIGHT - self.mountain_img.get_height() - 300))
            self.screen.blit(self.pine1_img, ((x * width) - Config.bg_scroll * 0.7,
                                              Config.SCREEN_HEIGHT - self.pine1_img.get_height() - 150))
            self.screen.blit(self.pine2_img, ((x * width) - Config.bg_scroll * 0.8,
                                              Config.SCREEN_HEIGHT - self.pine2_img.get_height()))

    # function to reset level
    def reset_level(self):
        self.enemy_group.empty()
        self.bullet_group.empty()
        self.grenade_group.empty()
        self.explosion_group.empty()
        self.item_box_group.empty()
        self.decoration_group.empty()
        self.water_group.empty()
        self.exit_group.empty()

        # create empty tile list
        data = []
        for row in range(Config.ROWS):
            r = [-1] * Config.COLS
            data.append(r)

        return data

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))  # Clear screen

            self.clock.tick(self.FPS)

            if self.start_game == False:
                self.screen.fill(self.BG)
                if self.start_button.draw(self.screen):
                    self.start_game = True
                if self.exit_button.draw(self.screen):
                    self.running = False

            else:
                self.draw_bg()
                # show player health
                self.health_bar.draw(self.player.health, self.screen)
                # show ammo
                self.draw_text(f'AMMO: ', Config.get_font(), Config.WHITE, 10, 35)
                for i in range(self.player.ammo):
                    self.screen.blit(self.bullet_img, (90 + (i * 10), 40))
                # show grenades
                self.draw_text(f'GRENADES: ', Config.get_font(), Config.WHITE, 10, 60)
                for i in range(self.player.grenades):
                    self.screen.blit(self.grenade_img, (135 + (i * 15), 60))

                self.player.update()
                # Draw player
                self.player.draw(self.screen)

                for enemy in Config.enemy_group:
                    enemy.ai(self.player, self.world)
                    enemy.update()
                    enemy.draw(self.screen)

                # update and draw world
                self.decoration_group.update()
                self.water_group.update()
                self.exit_group.update()
                self.world.draw(self.screen)
                self.decoration_group.draw(self.screen)
                self.water_group.draw(self.screen)
                self.exit_group.draw(self.screen)

                # update and draw bullet
                self.bullet_group.update(self.player, self.enemy, self.world)
                self.bullet_group.draw(self.screen)
                # update and draw grenade
                self.grenade_group.update(self.world)
                self.grenade_group.draw(self.screen)
                self.explosion_group.update()
                self.explosion_group.draw(self.screen)
                # update and draw item box
                self.item_box_group.update(self.player)
                self.item_box_group.draw(self.screen)

                # update player actions
                if self.player.alive:
                    if self.shoot:  # Only shoot when Space is pressed
                        self.player.shoot()
                    # throw grenades
                    elif self.grenade and self.grenade_thrown == False and self.player.grenades > 0:
                        self.grenade = Grenade(self.player.rect.centerx + (0.5 * self.player.rect.size[0] *
                                                                           self.player.direction), self.player.rect.top,
                                               self.player.direction,
                                               self.player)
                        self.grenade_group.add(self.grenade)
                        # reduce grenades
                        self.player.grenades -= 1
                        self.grenade_thrown = True

                    if self.player.in_air:
                        self.player.update_action(2)  # 2: jump
                    elif self.moving_left or self.moving_right:
                        self.player.update_action(1)  # 1: run
                    else:
                        self.player.update_action(0)  # 0: idle
                    if self.moving_left or self.moving_right:
                        Config.screen_scroll, level_complete = self.player.move(self.moving_left, self.moving_right, self.world)
                        print(f"Screen Scroll: {Config.screen_scroll}, Level Complete: {level_complete}")

                        Config.bg_scroll -= Config.screen_scroll
                        if level_complete:
                            Config.level += 1
                            Config.bg_scroll = 0
                            world_data = self.reset_level()
                            if Config.level <= Config.MAXS_LEVELS:
                                with open(f'level_{Config.level}_data.csv', newline='') as csvfile:
                                    reader = csv.reader(csvfile, delimiter=',')
                                    for x, row in enumerate(reader):
                                        for y, tile in enumerate(row):
                                            world_data[x][y] = int(tile)

                                self.world = World()
                                self.player, self.health_bar = self.world.process_data(world_data)

                    elif not self.moving_left and not self.moving_right:
                        Config.screen_scroll = 0
                else:
                    Config.screen_scroll = 0
                    if self.restart_button.draw(self.screen):
                        Config.bg_scroll = 0
                        world_data = self.reset_level()
                        # load in level data and create world
                        with open(f'level_{Config.level}_data.csv', newline='') as csvfile:
                            reader = csv.reader(csvfile, delimiter=',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)

                        self.world = World()
                        self.player, self.health_bar = self.world.process_data(world_data)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.moving_left = True
                    if event.key == pygame.K_d:
                        self.moving_right = True
                    if event.key == pygame.K_SPACE:
                        self.shoot = True
                    if event.key == pygame.K_q:
                        self.grenade = True
                    if event.key == pygame.K_w and self.player.alive:
                        self.player.jump = True
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.moving_left = False
                    if event.key == pygame.K_d:
                        self.moving_right = False
                    if event.key == pygame.K_SPACE:
                        self.shoot = False
                    if event.key == pygame.K_q:
                        self.grenade = False
                        self.grenade_thrown = False

            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()

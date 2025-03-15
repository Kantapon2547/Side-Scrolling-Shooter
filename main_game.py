import pygame
from character import Soldier
from grenades import Grenade
from item import Item
from game_config import Config
from health_bar import HealthBar


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
        self.bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
        self.grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()

        self.clock = pygame.time.Clock()
        self.FPS = 60

        self.BG = (144, 201, 120)
        # self.BG = (255, 253, 208)

        self.bullet_group = Config.bullet_group
        self.grenade_group = Config.grenade_group
        self.explosion_group = Config.explosion_group
        self.enemy_group = Config.enemy_group
        self.item_box_group = Config.item_box_group

        item_box = Item('Health', 100, 250)
        self.item_box_group.add(item_box)
        item_box = Item('Ammo', 400, 250)
        self.item_box_group.add(item_box)
        item_box = Item('Grenade', 500, 250)
        self.item_box_group.add(item_box)

        # Create player instance
        self.player = Soldier('player', 200, 200, 3, 5, 20, 5)
        self.health_bar = HealthBar(10, 10, self.player.health, self.player.health)
        self.enemy = Soldier('enemy', 400, 200, 3, 5, 20, 0)
        self.enemy2 = Soldier('enemy', 300, 300, 3, 5, 20, 0)
        self.enemy_group.add(self.enemy)
        self.enemy_group.add(self.enemy2)

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def draw_bg(self):
        self.screen.fill(self.BG)
        pygame.draw.line(self.screen, Config.RED, (0, 300), (Config.SCREEN_WIDTH, 300))

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))  # Clear screen

            self.clock.tick(self.FPS)

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

            for self.enemy in Config.enemy_group:
                self.enemy.update()
                self.enemy.draw(self.screen)

            # update and draw bullet
            self.bullet_group.update(self.player, self.enemy)
            self.bullet_group.draw(self.screen)
            # update and draw grenade
            self.grenade_group.update()
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
                                           self.player.direction), self.player.rect.top, self.player.direction,
                                           self.player)
                    self.grenade_group.add(self.grenade)
                    #reduce grenades
                    self.grenade_thrown = True
                    self.player.grenades -= 1

                if self.player.in_air:
                    self.player.update_action(2)  # 2: jump
                elif self.moving_left or self.moving_right:
                    self.player.update_action(1)  # 1: run
                else:
                    self.player.update_action(0)  # 0:idle
                self.player.move(self.moving_left, self.moving_right)

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

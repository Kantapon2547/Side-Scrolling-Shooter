import pygame
from character import Soldier
from bullet import Bullet
from game_config import Config


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        pygame.display.set_caption("Shooter")
        self.running = True
        self.moving_left = False
        self.moving_right = False
        self.shoot = False

        self.clock = pygame.time.Clock()
        self.FPS = 60

        self.BG = (144, 201, 120)
        # self.BG = (255, 253, 208)
        self.RED = (255, 0, 0)

        # Create player instance
        self.player = Soldier('player', 200, 200, 3, 5, 20)
        self.enemy = Soldier('enemy', 400, 200, 3, 5, 20)

        self.bullet_group = Config.bullet_group

    def draw_bg(self):
        self.screen.fill(self.BG)
        pygame.draw.line(self.screen, self.RED, (0, 300), (Config.SCREEN_WIDTH, 300))

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))  # Clear screen

            self.clock.tick(self.FPS)

            self.draw_bg()

            self.player.update()
            # Draw player
            self.player.draw(self.screen)

            self.enemy.update()
            self.enemy.draw(self.screen)

            # update and draw bullet
            self.bullet_group.update(self.player, self.enemy)
            self.bullet_group.draw(self.screen)

            # update player actions
            if self.player.alive:
                if self.shoot:  # Only shoot when Space is pressed
                    self.player.shoot()

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

            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()

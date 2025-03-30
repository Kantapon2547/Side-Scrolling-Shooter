import pygame
import button
import csv
from game_config import Config


class Level:
    def __init__(self):
        pygame.init()

        self.LOWER_MARGIN = 100
        self.SIDE_MARGIN = 300

        self.screen = pygame.display.set_mode(
            (Config.SCREEN_WIDTH + self.SIDE_MARGIN, Config.SCREEN_HEIGHT + self.LOWER_MARGIN))
        pygame.display.set_caption('Level Editor')

        self.MAX_COLS = 150
        self.level = 0
        self.current_tile = 0
        self.scroll_left = False
        self.scroll_right = False
        self.scroll = 0
        self.scroll_speed = 1

        # Load images
        self.pine1_img = pygame.image.load('img/Background/pine1.png').convert_alpha()
        self.pine2_img = pygame.image.load('img/Background/pine2.png').convert_alpha()
        self.mountain_img = pygame.image.load('img/Background/mountain.png').convert_alpha()
        self.sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()

        # Store tiles in a list
        self.img_list = []
        for x in range(Config.TILE_TYPE):
            img = pygame.image.load(f'img/tile/{x}.png').convert_alpha()
            img = pygame.transform.scale(img, (Config.TILE_SIZE, Config.TILE_SIZE))
            self.img_list.append(img)

        self.save_img = pygame.image.load('img/save_btn.png').convert_alpha()
        self.load_img = pygame.image.load('img/load_btn.png').convert_alpha()

        # Define colors
        self.GREEN = (144, 201, 120)
        self.WHITE = (255, 255, 255)
        self.RED = (200, 25, 25)

        # Define font
        self.font = pygame.font.SysFont('Futura', 30)

        # Create empty tile list
        self.world_data = [[-1] * self.MAX_COLS for _ in range(Config.ROWS)]

        # Create ground
        for tile in range(self.MAX_COLS):
            self.world_data[Config.ROWS - 1][tile] = 0

        # Create buttons
        self.save_button = button.Button(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT + self.LOWER_MARGIN - 50,
                                         self.save_img, 1)
        self.load_button = button.Button(Config.SCREEN_WIDTH // 2 + 200, Config.SCREEN_HEIGHT + self.LOWER_MARGIN - 50,
                                         self.load_img, 1)

        # Tile selection buttons
        self.button_list = []
        button_col, button_row = 0, 0
        for i in range(len(self.img_list)):
            tile_button = button.Button(Config.SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50,
                                        self.img_list[i], 1)
            self.button_list.append(tile_button)
            button_col += 1
            if button_col == 3:
                button_row += 1
                button_col = 0

    def draw_text(self, text, x, y):
        img = self.font.render(text, True, self.WHITE)
        self.screen.blit(img, (x, y))

    def draw_bg(self):
        self.screen.fill(self.GREEN)
        width = self.sky_img.get_width()
        for x in range(4):
            self.screen.blit(self.sky_img, ((x * width) - self.scroll * 0.5, 0))
            self.screen.blit(self.mountain_img, ((x * width) - self.scroll * 0.6,
                                                 Config.SCREEN_HEIGHT - self.mountain_img.get_height() - 300))
            self.screen.blit(self.pine1_img, ((x * width) - self.scroll * 0.7,
                                              Config.SCREEN_HEIGHT - self.pine1_img.get_height() - 150))
            self.screen.blit(self.pine2_img, ((x * width) - self.scroll * 0.8,
                                              Config.SCREEN_HEIGHT - self.pine2_img.get_height()))

    def draw_grid(self):
        for c in range(self.MAX_COLS + 1):
            pygame.draw.line(self.screen, self.WHITE, (c * Config.TILE_SIZE - self.scroll, 0),
                             (c * Config.TILE_SIZE - self.scroll, Config.SCREEN_HEIGHT))
        for c in range(Config.ROWS + 1):
            pygame.draw.line(self.screen, self.WHITE, (0, c * Config.TILE_SIZE),
                             (Config.SCREEN_WIDTH, c * Config.TILE_SIZE))

    def draw_world(self):
        for y, row in enumerate(self.world_data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    self.screen.blit(self.img_list[tile], (x * Config.TILE_SIZE - self.scroll, y * Config.TILE_SIZE))

    def run(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)
            self.draw_bg()
            self.draw_grid()
            self.draw_world()

            self.draw_text(f'Level: {self.level}', 10, Config.SCREEN_HEIGHT + self.LOWER_MARGIN - 90)
            self.draw_text('Press UP or DOWN to change level', 10, Config.SCREEN_HEIGHT + self.LOWER_MARGIN - 60)

            if self.save_button.draw(self.screen):
                with open(f'level_{self.level}_data.csv', 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerows(self.world_data)

            if self.load_button.draw(self.screen):
                # load in level data
                # reset scroll back to the start of the level
                self.scroll = 0
                with open(f'level_{self.level}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    # self.world_data = [[int(tile) for tile in row] for row in reader]
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            self.world_data[x][y] = int(tile)

            # draw tile panel and tiles
            pygame.draw.rect(self.screen, self.GREEN, (Config.SCREEN_WIDTH, 0, self.SIDE_MARGIN, Config.SCREEN_HEIGHT))

            # choose a tile
            button_count = 0
            for button_count, i in enumerate(self.button_list):
                if i.draw(self.screen):
                    self.current_tile = button_count

            # highlight the selected tile
            pygame.draw.rect(self.screen, self.RED, self.button_list[self.current_tile].rect, 3)

            # scroll the map
            if self.scroll_left == True and self.scroll > 0:
                self.scroll -= 5 * self.scroll_speed
            if self.scroll_right == True and self.scroll < (self.MAX_COLS * Config.TILE_SIZE) - Config.SCREEN_WIDTH:
                self.scroll += 5 * self.scroll_speed

            # add new tiles to the screen
            # get mouse position
            pos = pygame.mouse.get_pos()
            x = (pos[0] + self.scroll) // Config.TILE_SIZE
            y = pos[1] // Config.TILE_SIZE

            # check that the coordinates are within the tile area
            if pos[0] < Config.SCREEN_WIDTH and pos[1] < Config.SCREEN_HEIGHT:
                # update tile value
                if pygame.mouse.get_pressed()[0] == 1:
                    if self.world_data[y][x] != self.current_tile:
                        self.world_data[y][x] = self.current_tile
                if pygame.mouse.get_pressed()[2] == 1:
                    self.world_data[y][x] = -1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.level += 1
                    if event.key == pygame.K_DOWN and self.level > 0:
                        self.level -= 1
                    if event.key == pygame.K_LEFT:
                        self.scroll_left = True
                    if event.key == pygame.K_RIGHT:
                        self.scroll_right = True
                    if event.key == pygame.K_RSHIFT:
                        self.scroll_speed = 5

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.scroll_left = False
                    if event.key == pygame.K_RIGHT:
                        self.scroll_right = False
                    if event.key == pygame.K_RSHIFT:
                        self.scroll_speed = 1

            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    level = Level()
    level.run()

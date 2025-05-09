import pygame
import os
import csv
from game_config import Config
from bullet import Bullet
import random
import time

# Initialize the CSV logging (if not already initialized)
DATA_FILE = 'data_collection.csv'

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Health Before', 'Health After', 'Health Lost', 'Bullets Fired',
                         'Deaths', 'Grenades Thrown'])


class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, grenades):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.grenades = grenades
        self.health = 100
        self.max_health = self.health
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.bullet_group = pygame.sprite.Group()
        # ai specific variables
        self.move_counter = 0
        self.idling = False
        self.idling_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        # data_collection
        self.bullets_fired = 0
        self.deaths_per_level = 0
        self.grenades_thrown = 0
        self.last_shoot_time = time.time()  # To track when the last shot was fired
        self.data_collection_interval = 60
        self.current_level = Config.level
        self.prev_grenades = self.grenades


        # load all images for the players
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            # reset temporary list of images
            temp_list = []
            # count number of files in the folder
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.font = pygame.font.SysFont('Arial', 30)

        self.enemy = None

        # Initialize last health value for tracking health changes
        if not hasattr(self, '_last_health'):
            self._last_health = self.health

    def update(self):
        self.update_animation()
        self.check_alive()
        # Display current level on the screen

        # Track health change only for player
        if self.char_type == 'player':
            # Log the shot data
            if time.time() - self.last_shoot_time >= self.data_collection_interval:
                self.last_shoot_time = time.time()  # Update the last shoot time
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                # Write the data to the CSV
                with open(DATA_FILE, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([timestamp, self.bullets_fired, self.ammo])

            if self.grenades < self.prev_grenades:
                self.grenades_thrown += (self.prev_grenades - self.grenades)
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

                with open(DATA_FILE, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([timestamp, self.grenades_thrown])

                print(f"Grenade thrown! Total: {self.grenades_thrown}")

            self.prev_grenades = self.grenades  # Always update

            if self.health < self._last_health:
                damage_taken = self._last_health - self.health
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

                # Check if file exists or is empty to write the header once
                if not os.path.exists(DATA_FILE) or os.stat(DATA_FILE).st_size == 0:
                    with open(DATA_FILE, 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([
                            'Timestamp',
                            'Level',
                            'Previous Health',
                            'Current Health',
                            'Health Lost',
                            'Bullets Fired',
                            'Deaths',
                            'Grenades Thrown'
                        ])

                # Now append the data
                with open(DATA_FILE, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([
                        timestamp,
                        self.current_level,
                        self._last_health,
                        self.health,
                        damage_taken,
                        self.bullets_fired,
                        self.deaths_per_level,
                        self.grenades_thrown
                    ])

                self._last_health = self.health  # Update to new health

        # update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right, world):
        # reset movement variables
        screen_scroll = 0
        dx = 0
        dy = 0

        # assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # apply gravity
        self.vel_y += Config.GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10

        # Update vertical position
        dy += self.vel_y

        # check collision with floor
        for tile in world.obstacle_list:
            # check collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            # check for collision in the y direction
                if self.char_type == 'enemy':
                    self.direction *= -1
                    self.move_counter = 0

            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if below the ground, i.e. jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        # check for collision with water
        if pygame.sprite.spritecollide(self, Config.water_group, False):
            self.health = 0

        # check for collision with exit
        level_complete = False
        if pygame.sprite.spritecollide(self, Config.exit_group, False):
            level_complete = True

        # check if fallen off the map
        if self.rect.bottom > Config.SCREEN_HEIGHT:
            self.health = 0

        # check if going off the edges of the screen
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > Config.SCREEN_WIDTH:
                dx = 0

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        # update scroll based on player position
        if self.char_type == 'player':
            if (self.rect.right > Config.SCREEN_WIDTH - Config.SCROLL_THRESH and Config.bg_scroll < (
                    world.level_length * Config.TILE_SIZE) - Config.SCREEN_WIDTH) \
                    or (self.rect.left < Config.SCROLL_THRESH and Config.bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20  # set the cooldown to prevent shooting too fast
            bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction),
                            self.rect.centery, self.direction)  # No need to pass shooter now
            Config.bullet_group.add(bullet)  # add the bullet to the bullet group
            self.ammo -= 1  # reduce the ammo by 1
            self.bullets_fired += 1  # Increase bullets fired counter
            Config.shot_fx.play()

            return bullet  # Return the bullet

    def ai(self, player, world):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)  # 0: idle
                self.idling = True
                self.idling_counter = 50
            # check if the ai in near the player
            if self.vision.colliderect(player.rect):
                # stop running and face the player
                self.update_action(0)  # 0: idle
                # shoot
                self.shoot()
                # randomly throw grenade if available
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right, world)
                    self.update_action(1)  # 1: run
                    self.move_counter += 1
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > Config.TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                    else:
                        self.idling_counter -= 1
                        if self.idling_counter <= 0:
                            self.idling = False

        # Adjust AI for screen scroll
        self.rect.x += Config.screen_scroll

    def update_animation(self):
        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > Config.ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)
            self.log_death()
            if self.char_type == 'player':  # Ensure only player death counts
                self.deaths_per_level += 1  # Increment death count when player dies

    def log_death(self):
        # Log death information to CSV (if it's a player character)
        if self.char_type == 'player':
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            with open(DATA_FILE, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([timestamp, self._last_health, self.health, 0, self.bullets_fired,
                                 self.deaths_per_level, self.grenades_thrown])

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

from pygame.math import Vector2
from utils import load_sprite, wrap_position, get_random_pos
from pygame.transform import rotozoom
import pygame

UP = Vector2(0, -1)


class game_object():
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width()/2
        self.velocity = Vector2((velocity))
        self.i = 0
        self.current_box = (300, 300)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface, speed):

        self.i += 1
        if self.i == speed:
            self.position = wrap_position(self.position+self.velocity, surface)
            self.i = 0

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius


class snake_head(game_object):

    def __init__(self, position):
        super().__init__(position, load_sprite("snake"), Vector2(0, -1))
        self.direction = Vector2(UP)
        self.head_direction = "up"
        self.moving = "up"
        self.state = False
        self.x = 0

    def rotate(self, movement, direction):
        set_to_zero = self.direction.angle_to(UP)
        self.direction.rotate_ip(set_to_zero)
        self.direction.rotate_ip(direction)
        self.velocity = movement

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def move_in_grid(self):
        if self.position[0] % 30 == 0 and self.position[1] % 30 == 0:
            self.current_box = self.position

        if self.moving == "up":

            if 1 < self.position[1] % 30 < 15:

                if self.head_direction == "left":
                    self.position[0] = self.position[0] - \
                        (self.current_box[1] - self.position[1])
                    self.position[1] = self.current_box[1]
                    self.rotate((-1, 0), 270)
                    self.moving = "left"
                    self.x = self.position[0] % 30

                elif self.head_direction == "right":
                    self.position[0] = self.position[0] + \
                        (self.current_box[1] - self.position[1])
                    self.position[1] = self.current_box[1]
                    self.rotate((1, 0), 90)
                    self.moving = "right"
                    self.x = self.position[0] % 30

                else:
                    pass
            else:
                pass

        elif self.moving == "down":
            if 29 > self.position[1] % 30 > 15:
                if self.head_direction == "left":
                    self.position[0] = self.position[0] - \
                        (self.position[1] - self.current_box[1])
                    self.position[1] = self.current_box[1]
                    self.rotate((-1, 0), 270)
                    self.moving = "left"
                    self.x = self.position[0] % 30

                elif self.head_direction == "right":
                    self.position[0] = self.position[0] + \
                        (self.position[1] - self.current_box[1])
                    self.position[1] = self.current_box[1]
                    self.rotate((1, 0), 90)
                    self.moving = "right"
                    self.x = self.position[0] % 30

                else:
                    pass
            else:
                pass

        elif self.moving == "left":
            if 1 < self.position[0] % 30 < 15:
                if self.head_direction == "up":
                    self.position[1] = self.position[1] - \
                        (self.current_box[0] - self.position[0])
                    self.position[0] = self.current_box[0]
                    self.rotate((0, -1), 0)
                    self.moving = "up"
                    self.x = self.position[1] % 30

                elif self.head_direction == "down":
                    self.position[1] = self.position[1] + \
                        (self.current_box[0] - self.position[0])
                    self.position[0] = self.current_box[0]
                    self.rotate((0, 1), 180)
                    self.moving = "down"
                    self.x = self.position[1] % 30

                else:
                    pass
            else:
                pass

        elif self.moving == "right":
            if 29 > self.position[0] % 30 > 15:
                if self.head_direction == "up":
                    self.position[1] = self.position[1] - \
                        (self.position[0] - self.current_box[0])
                    self.position[0] = self.current_box[0]
                    self.rotate((0, -1), 0)
                    self.moving = "up"
                    self.x = self.position[1] % 30

                elif self.head_direction == "down":
                    self.position[1] = self.position[1] + \
                        (self.position[0] - self.current_box[0])
                    self.position[0] = self.current_box[0]
                    self.rotate((0, 1), 180)
                    self.moving = "down"
                    self.x = self.position[1] % 30

                else:
                    pass
            else:
                pass


class nommers(game_object):

    def __init__(self):
        super().__init__(get_random_pos(), load_sprite("hamburger"), Vector2(0, 0))


class snake_body(game_object):

    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("circle"), Vector2(0, 0))
        self.velocity = velocity
        if velocity == (0, 1):
            self.position[1] -= 28
        if velocity == (0, -1):
            self.position[1] += 28
        if velocity == (1, 0):
            self.position[0] -= 28
        if velocity == (-1, 0):
            self.position[0] += 28


class Button():
    def __init__(self, x, y, image):
        self.image = pygame.image.load(
            f"assets/buttons/{image}.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def button_func(self, screen):

        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):

            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True

        screen.blit(self.image, (self.rect.x, self.rect.y))


class menu_button(Button):
    def __init__(self):
        super().__init__(325, 400, "settings")


class restart_button(Button):
    def __init__(self):
        super().__init__(210, 400, "restart")


class play_button(Button):
    def __init__(self):
        super().__init__(380, 300, "play-button")


class pause_button(Button):
    def __init__(self):
        super().__init__(235, 140, "pause")

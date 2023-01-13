import pygame
from models import pause_button, restart_button, menu_button, play_button
from utils import get_highscores


class Menu():
    def __init__(self):

        # add snake on menu
        self.snake_pic = pygame.image.load("assets/sprites/scared.png")
        self.snake_pic.get_rect()

        # import name box
        self.base_font = pygame.font.Font(None, 32)
        self.err_font = pygame.font.Font(None, 20)
        self.input_rect_border = pygame.Rect(135, 310, 210, 37)
        self.input_rect = pygame.Rect(140, 315, 130, 27)
        self.color = pygame.Color('chartreuse4')
        self.user_text = ""
        self.err_message_state = False

        # import play button
        self.play_button = play_button()

        # highscores data
        self.highscores = get_highscores()

    def menu_draw(self, screen):

        # make black screen
        pygame.draw.rect(screen, (0, 0, 0),
                         pygame.Rect(0, 0, 602, 602))

        # draw snake
        screen.blit(self.snake_pic, (110, 20))

        # draw Name :
        self.name_title_box = self.base_font.render(
            "Name: ", True, (255, 255, 255))
        screen.blit(self.name_title_box,
                    (self.input_rect.x-80, self.input_rect.y+5))

        # draw import box
        pygame.draw.rect(screen, self.color, self.input_rect_border)
        pygame.draw.rect(screen, "black", self.input_rect)
        self.text_surface = self.base_font.render(
            self.user_text, True, (255, 255, 255))
        screen.blit(self.text_surface,
                    (self.input_rect.x+5, self.input_rect.y+5))
        self.input_rect.w = max(200, self.text_surface.get_width()+10)

        # error message
        if self.err_message_state == True:
            self.err_message = self.err_font.render(
                "Enter a username", True, (255, 0, 0))
            screen.blit(self.err_message, (140, 350))

        # play button
        self.play_button.button_func(screen)

        # highscores title
        self.highscore_title = self.base_font.render(
            "HIGHSCORES", True, (255, 255, 255))
        screen.blit(self.highscore_title, (165, 390))

        # highscore table
        for i in range(0, 8):
            self.highscore_row = self.base_font.render(
                f"Position {i+1} :", True, (0, 255, 255))
            screen.blit(self.highscore_row, (20, 450+(30*i)))

            self.highscore_name = self.base_font.render(
                f"{self.highscores[i][1]}", True, (0, 255, 255))
            screen.blit(self.highscore_name, (250, 450+(30*i)))

            self.highscore_value = self.base_font.render(
                f"{self.highscores[i][2]}", True, (0, 255, 255))
            screen.blit(self.highscore_value, (400, 450+(30*i)))


class Background():
    def __init__(self):

        # background surface
        self.background = pygame.surface.Surface((602, 602))

        # grid maker
        self.border = []
        self.background_line_ud = 15
        self.background_line_lr = 15
        while self.background_line_ud <= 900:
            pygame.draw.line(
                self.background, (0, 0, 100), (self.background_line_ud, 0), (self.background_line_ud, 600), 2)
            pygame.draw.line(
                self.background, (0, 0, 100), (0, self.background_line_lr), (600, self.background_line_lr), 2)
            self.background_line_ud += 30
            self.background_line_lr += 30

        # borders
        pygame.draw.line(self.background, (0, 0, 100), (0, 0), (0, 602), 30)
        pygame.draw.line(self.background, (0, 0, 100),
                         (602, 0), (602, 602), 32)
        pygame.draw.line(self.background, (0, 0, 100), (0, 0), (602, 0), 30)
        pygame.draw.line(self.background, (0, 0, 100),
                         (0, 602), (602, 602), 32)

    def draw(self, screen, snake):
        screen.blit(snake, (115, 20))


class Pause():
    def __init__(self):

        # create buttons
        self.buttons = []
        self.pause_button = pause_button()
        self.restart_button = restart_button()
        self.settings_button = menu_button()
        self.buttons.append(self.restart_button)
        self.buttons.append(self.pause_button)
        self.buttons.append(self.settings_button)
        self.base_font = pygame.font.Font(None, 64)

    def draw(self, screen):

        # black screen
        pygame.draw.rect(screen, (0, 0, 0),
                         pygame.Rect(0, 0, 602, 602))

        # draw pause on screen
        pygame.draw.rect(screen, (0, 0, 255),
                         pygame.Rect(150, 75, 300, 450))
        pygame.draw.rect(screen, (255, 255, 255),
                         pygame.Rect(175, 100, 250, 400))

        # type PAUSED
        self.paused_text = self.base_font.render("PAUSED", True, (0, 0, 0))
        screen.blit(self.paused_text, (210, 300))

        # check for buttons
        for button in self.buttons:
            button.button_func(screen)

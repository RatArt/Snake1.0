import pygame
from models import snake_body, snake_head, nommers
from game_states import Menu, Background, Pause
from utils import print_text, insert_into_db, get_highscores


class snake_try():
    def __init__(self):
        self._init_pygame()
        self.pause = True
        self.speed = 1
        self.screen = pygame.display.set_mode((602, 602))
        self.clock = pygame.time.Clock()
        self.background = Background()
        self.snake_parts = []
        self.snake_head = snake_head((300, 300))
        self.snake_parts.append(self.snake_head)
        self.nom = nommers()
        self.font = pygame.font.Font(None, 64)
        self.message = ""
        self.menu = True
        self.menu_screen = Menu()
        self.pause_screen = Pause()
        self.user_name = ""
        self.pos_check = 0
        self.check_num = 0

    def main_loop(self):
        while True:
            self.handle_input()
            self.process_game_logic()
            self.draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Pomalu snejksi")

    def _get_game_objects(self):

        # adding snake body
        game_objects = [*self.snake_parts]

        # adding burgers
        if self.nom:
            game_objects.append(self.nom)
        return game_objects

    def handle_input(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            # swaping between game, menu and pause
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self.menu == False:
                    if self.pause == True:
                        self.pause = False
                    else:
                        self.pause = True
                if self.menu == True:
                    quit()

            # controls in menu
            if self.menu == True:

                # typing name
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.menu_screen.user_text = self.menu_screen.user_text[:-1]
                    else:
                        self.menu_screen.user_text += event.unicode

            # game input
            if self.pause == False and self.menu == False:

                is_key_pressed = pygame.key.get_pressed()
                if self.snake_head.x == 0:

                    if is_key_pressed[pygame.K_RIGHT]:
                        if self.snake_head.velocity != (-1, 0):
                            self.snake_head.head_direction = "right"

                    elif is_key_pressed[pygame.K_LEFT]:
                        if self.snake_head.velocity != (1, 0):
                            self.snake_head.head_direction = "left"

                    elif is_key_pressed[pygame.K_UP]:
                        if self.snake_head.velocity != (0, 1):
                            self.snake_head.head_direction = "up"

                    elif is_key_pressed[pygame.K_DOWN]:
                        if self.snake_head.velocity != (0, -1):
                            self.snake_head.head_direction = "down"

                else:
                    pass

    def process_game_logic(self):

        # main game logic
        if self.pause == False and self.menu == False:
            for game_object in self._get_game_objects():
                game_object.move(self.screen, self.speed)

            # move snake in a grid
            if self.snake_head.state == False:
                if self.snake_head.x > 0:
                    self.snake_head.x -= 1
                self.snake_head.move_in_grid()

            # snake body follows the part infront of it
            for i in range(1, len(self.snake_parts)):

                if self.snake_parts[i].position[0] % 30 == 0 and self.snake_parts[i].position[1] % 30 == 0:
                    self.pos_check = self.snake_parts[i-1].position - \
                        self.snake_parts[i].position

                    # calculating velocity for each body part
                    if self.pos_check[0] == 28:
                        self.snake_parts[i].velocity = (1, 0)
                    elif self.pos_check[0] == -28:
                        self.snake_parts[i].velocity = (-1, 0)
                    elif self.pos_check[1] == 28:
                        self.snake_parts[i].velocity = (0, 1)
                    elif self.pos_check[1] == -28:
                        self.snake_parts[i].velocity = (0, -1)

            # if snake is alive check for collision
            if self.snake_head.state == False:

                # win screen
                if len(self.snake_parts) == 399:
                    self.message = "You... win? tf.. bro"
                    insert_into_db(
                        self.user_name, len(self.snake_parts)-1)
                    self.menu_screen.highscores = get_highscores()
                    self.snake_head.state = True

                for i in range(2, len(self.snake_parts)):

                    # snake collision with its body
                    if self.snake_head.collides_with(self.snake_parts[i]):
                        self.message = f"You lost with Score {len(self.snake_parts)-1}"
                        for _ in self.snake_parts:
                            _.velocity = (0, 0)
                        insert_into_db(
                            self.user_name, len(self.snake_parts)-1)
                        self.menu_screen.highscores = get_highscores()
                        print("Score inserted and updated")
                        self.snake_head.state = True

                # snake collision with border
                if self.snake_head.position[0] == 0 or self.snake_head.position[1] == 0 or self.snake_head.position[0] == 602 or self.snake_head.position[1] == 602:
                    self.message = f"You lost with Score {len(self.snake_parts)-1}"
                    self.snake_head.velocity = (0, 0)
                    for _ in self.snake_parts:
                        _.velocity = (0, 0)
                    insert_into_db(self.user_name, len(self.snake_parts)-1)
                    self.menu_screen.highscores = get_highscores()
                    print("Score inserted and updated")
                    self.snake_head.state = True

            # BURGER PART (nom = burger)
            if self.nom == None:

                # if no burger = add part to snake body and spawn a new burger
                snake_part = snake_body(
                    self.snake_parts[len(self.snake_parts)-1].position, self.snake_parts[len(self.snake_parts)-1].velocity)
                self.snake_parts.append(snake_part)
                self.nom = nommers()
                self.game_objects = [*self.snake_parts]

            # if burger in border == True > respawn a burger
            if self.nom.position[0] == 0 or self.nom.position[1] == 0 or self.nom.position[0] == 570 or self.nom.position[1] == 570:
                self.nom = None
                self.nom = nommers()

            for i in range(1, len(self.snake_parts)-1):
                if self.nom.collides_with(self.snake_parts[i]):
                    self.nom = None
                    self.nom = nommers()

            # když had pos == burger pos > burger gone
            if self.snake_head.collides_with(self.nom):
                self.nom = None

        # buttons in pause mode
        if self.pause == True and self.menu == False:

            # open menu button
            if self.pause_screen.settings_button.clicked == True:
                self.menu = True
                self.pause_screen.settings_button.clicked = False

            # restart game button
            if self.pause_screen.restart_button.clicked == True:
                self.snake_head = snake_head((300, 300))
                self.snake_head.head_direction = "up"
                self.snake_parts = []
                self.snake_parts.append(self.snake_head)
                self.message = ""
                self.snake_head.state = False
                self.pause_screen.restart_button.clicked = False

            # resume the game button
            if self.pause_screen.pause_button.clicked == True:
                self.pause = False
                self.pause_screen.pause_button.clicked = False

        # buttons in menu mode
        if self.menu == True:

            # from menu to pause
            if self.menu_screen.play_button.clicked == True:
                if len(self.menu_screen.user_text) > 0:
                    self.menu = False
                    self.screen = pygame.display.set_mode((602, 602))
                    self.menu_screen.play_button.clicked = False
                    self.menu_screen.err_message_state = False
                    self.user_name = self.menu_screen.user_text
                    print(len(self.user_name))

                else:
                    self.menu_screen.play_button.clicked = False
                    self.menu_screen.err_message_state = True

    def draw(self):

        # draw menu
        if self.menu == True:
            self.screen = pygame.display.set_mode((475, 700))
            self.menu_screen.menu_draw(self.screen)

        # draw pause
        if self.pause == True and self.menu == False:
            self.pause_screen.draw(self.screen)

        # draw game
        if self.pause == False and self.menu == False:
            self.screen.blit(self.background.background, (0, 0))
            for game_object in self._get_game_objects():
                game_object.draw(self.screen)

            if self.message:
                print_text(self.screen, self.message, self.font)

        # update screen
        pygame.display.flip()

        # max FPS
        self.clock.tick(100)

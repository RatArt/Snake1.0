from pygame.image import load
from pygame.math import Vector2
import random
from pygame import Color
import mysql
from mysql.connector import connection, Error
from db_config import db_login


def load_sprite(name, with_alpha=True):
    path = f"assets/sprites/{name}.png"
    loaded_sprite = load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()


def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)


def get_random_pos():
    i = int(random.randint(0, 19) * 30)
    x = int(random.randint(0, 19) * 30)
    position = ((x, i))
    return position


def print_text(surface, text, font, color=Color("red4")):
    text_surface = font.render(text, True, color)

    rect = text_surface.get_rect()
    rect.center = Vector2(surface.get_size()) / 2

    surface.blit(text_surface, rect)


def insert_into_db(name, score):
    try:
        connection = mysql.connector.connect(host=db_login['db_host'],
                                             database=db_login['db_name'],
                                             user=db_login["db_username"],
                                             password=db_login['db_password'])

        if connection.is_connected():

            insert_into_highscores = """
            INSERT INTO High_Scores_Snake
            (Name, Score)
            VALUES ( %s, %s )
            """
            record = (name, score)

            db_info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_info)
            cursor = connection.cursor()
            cursor.execute(insert_into_highscores, record)
            connection.commit()

    except Error as e:
        print(e)


def get_highscores():
    try:
        connection = mysql.connector.connect(host=db_login['db_host'],
                                             database=db_login['db_name'],
                                             user=db_login["db_username"],
                                             password=db_login['db_password'])

        if connection.is_connected():

            fetch_top_5 = """
                        SELECT * FROM High_Scores_Snake
                        ORDER BY Score DESC
                        """

            db_info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_info)
            cursor = connection.cursor()
            cursor.execute(fetch_top_5)
            result = cursor.fetchmany(size=8)
            return result

    except Error as e:
        print(e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

import os
import sys
import pygame

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def load_image(path):
    return pygame.image.load(resource_path(path)).convert_alpha()


def load_sound(path):
    return pygame.mixer.Sound(resource_path(path))
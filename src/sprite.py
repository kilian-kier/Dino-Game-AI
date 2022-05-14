import os
import pygame


def load_image(name):
    fullname = os.path.join(os.path.join(
        os.path.dirname(__file__), 'imgs'), name)
    image = pygame.image.load(fullname).convert_alpha()
    return image


def load_sprite_sheet(sheet_name, nx, scale):
    fullname = os.path.join(os.path.join(
        os.path.dirname(__file__), 'imgs'), sheet_name)
    sheet = pygame.image.load(fullname)
    sheet = pygame.transform.scale(
        sheet, (int(sheet.get_width() * scale), int(sheet.get_height() * scale)))
    sheet = sheet.convert_alpha()

    sheet_rect = sheet.get_rect()

    image_list = []

    size_x = sheet_rect.width / nx
    size_y = sheet_rect.height

    for i in range(0, nx):
        rect = pygame.Rect((i * size_x, 0, size_x, size_y))
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image = image.convert_alpha()
        image.blit(sheet, (0, 0), rect)

        image_list.append(image)

    return image_list

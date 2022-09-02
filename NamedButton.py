import pygame as pg
from Button import Button


class NamedButton:
    def __init__(self, pos, width, name, font_pixel_size, associated_flag):
        self.name = name
        self.pos = pos
        self.width = width
        # init font
        pg.font.init()
        self.font_pixel_size = font_pixel_size
        self.font_size = int(12 * self.font_pixel_size / 16.0)
        self.font = pg.font.SysFont("Arial", self.font_size)
        self.font_color = (155, 155, 155)
        self.text_surface = self.font.render(f"{self.name}", True, self.font_color)
        # init button
        self.rel_but_size = 0.7
        self.button = Button(center=pg.Vector2(self.pos[0] + self.width - (self.text_surface.get_height() * (0.5)), self.pos[1] + int(self.text_surface.get_height() * 0.5)), size=int(self.text_surface.get_height() * self.rel_but_size), associated_flag=associated_flag)

    # draw function
    def draw(self, surf):
        surf.blit(self.text_surface, self.pos)
        self.button.draw(surf)

    # user event handler
    def event_handler(self, events, mouse_pos, keys_pressed, mouse_pressed):
        self.button.event_handler(events, mouse_pos, keys_pressed, mouse_pressed)

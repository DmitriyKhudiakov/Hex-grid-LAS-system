import pygame as pg


class Button:
    def __init__(self, center, size, associated_flag):
        # True - on, False - off
        self.state = False
        # it is list: list[0] - object, list[1] attribute name
        self.associated_flag = associated_flag
        
        # init geometry
        self.center = center
        self.size = size
        # relative border thickness
        self.b_th_rel = 0.1
        self.border_thickness = int(self.size * self.b_th_rel)
        # relative inner part size
        self.i_p_rel = 0.6
        self.inner_part = int(self.size * self.i_p_rel)
        
        # init colors
        self.border_color = (155, 155, 155)
        self.off_color = (185, 100, 100)
        self.on_color = (100, 185, 100)

    # draw function
    def draw(self, surf):
        pg.draw.rect(surf, self.border_color, pg.Rect(self.center[0] - self.size // 2, self.center[1] - self.size // 2, self.size, self.size), self.border_thickness)
        pg.draw.rect(surf, self.on_color if self.state else self.off_color, pg.Rect(self.center[0] - self.inner_part // 2, self.center[1] - self.inner_part // 2, self.inner_part, self.inner_part))

    # user event handler (android version)
    def event_handler(self, events, mouse_pos, keys_pressed, mouse_pressed):
        for event in events:
            if event.type == pg.MOUSEBUTTONUP:
                if pg.Rect(self.center[0] - self.size // 2, self.center[1] - self.size // 2, self.size, self.size).collidepoint(mouse_pos):
                    self.state = not self.state
                    if len(self.associated_flag) == 2:
                        setattr(self.associated_flag[0], self.associated_flag[1], self.state)
                    else:
                        getattr(self.associated_flag[0], self.associated_flag[1])[self.associated_flag[2]] = self.state

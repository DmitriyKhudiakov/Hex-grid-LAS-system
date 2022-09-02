import pygame as pg


class LineArrow:
    def __init__(self, size, pos, line_length):
        # geometey
        self.size = size
        self.pos = pos
        self.line_length = line_length
        # center of main rect
        self.center = self.pos + pg.Vector2(size, size) // 2
        # center of arrowed inner circle
        self.center_arrow = self.center
        self.rect = pg.Rect(self.pos[0], self.pos[1], self.size, self.size)
        in_rel_d = 0.7
        self.r = int(self.size * in_rel_d /2)
        self.line_width = int(self.r * 0.2)
        self.delta_arrow = pg.Vector2(0, -self.line_length)
        self.arrow_pos = self.center_arrow + self.delta_arrow
        self.delta_circle = pg.Vector2(self.r, 0)
        self.border_thickness = int(self.size *(1 - in_rel_d) / 4)
        
        #colors
        self.border_color = (155, 155, 155)
        self.arrow_color = (253, 198, 119)
        
        # flags
        # arrowed inner circle work like a cursor
        self.is_locked = False
    
    #funcrion draw cursor and arrowed line
    def draw(self, surf):
        pg.draw.rect(surf, self.border_color, self.rect, self.border_thickness)
        if self.is_locked:
            # triangle type
            pg.draw.polygon(surf, self.arrow_color, [(self.center_arrow - self.delta_circle), self.arrow_pos, (self.center_arrow + self.delta_circle)], self.line_width)
            # line type
            #pg.draw.line(surf, self.arrow_color, self.center_arrow, self.arrow_pos, self.line_width)
        pg.draw.circle(surf, self.arrow_color, self.center_arrow, self.r)
    
    # function handle user events
    def event_handler(self, events, mouse_pos, keys_pressed, mouse_pressed):
        if self.is_locked:
            # look condition in game class (change mouse pos)
            self.center_arrow = mouse_pos - self.delta_arrow
            self.arrow_pos = mouse_pos
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(mouse_pos):
                    self.is_locked = not self.is_locked
            if (event.type == pg.MOUSEBUTTONUP) and self.is_locked:
                self.is_locked = not self.is_locked
                self.center_arrow = self.center
    
    # decorator for main game handler. lock main mouse pos when flag is_locked activate ???

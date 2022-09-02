import pygame as pg
import math as m


N_SIDES = 6


class Cell:
    def __init__(self, layer, angle, step):
        # coordinates of cell on grid
        self.l = layer
        self.a = angle
        self.s = step
        # list of neighbours of cell (usually - N_SIDES,or less (None instead of another cell))
        self.nhs = [None for _ in range(N_SIDES)]
        # geometry params r_out, r_in - radiuses of outer and inner circles, vs - list of vertices
        self.center = None
        self.r_out = None
        self.r_in = None
        self.vs = [None for _ in range(N_SIDES)]
        # used colors
        self.border_color = (155, 155, 155)
        self.inside_color = (150, 23, 43)
        self.nh_color = (23, 150, 43)
        self.layer_color = (23, 43, 150)
        self.horizontal_color = (43, 150, 23)
        self.vertical_color = (78, 23, 97)
        self.dir_a_color = (156, 67, 145)
        # thickness of border
        self.border_thickness = 2
        # flags:
        # is mouse inside cell
        self.is_inside = False
        # is cell in neighbor state (defined/set not here)
        self.is_nh = False
        # is cell in layer state (defined/set not here) - layer state means have same l coordinate
        self.is_layer = False
        # is cell in horizontal state (defined/set not here) - relatively window
        self.is_horizontal = False
        # is cell in vertical state (defined/set not here) - relatively window
        self.is_vertical = False
        # is cell on same angle axes
        self.is_dir_a = False
    
    # function return True if pos coordinates inside cell and False otherwise
    def is_point_inside(self, pos):
        num = len(self.vs)
        x = pos[0]
        y = pos[1]
        j = num - 1
        c = False
        for i in range(num):
            if (x == self.vs[i][0]) and (y == self.vs[i][1]):
                # point is a corner
                return True
            if ((self.vs[i][1] > y) != (self.vs[j][1] > y)):
                slope = (x-self.vs[i][0])*(self.vs[j][1]-self.vs[i][1])-(self.vs[j][0]-self.vs[i][0])*(y-self.vs[i][1])
                if slope == 0:
                    # point is on boundary
                    return True
                if (slope < 0) != (self.vs[j][1] < self.vs[i][1]):
                    c = not c
            j = i
        return c
    
    # function drawing cell in self board position (used coordinates of vertices) on surf
    def draw(self, surf):
        # if mouse is inside cell, use special background color
        if self.is_inside:
            pg.draw.polygon(surf, self.inside_color, self.vs, 0)
            # disable flag every iteration
            self.is_inside = False
        # if cell in neighbor state, use special background color
        elif self.is_nh:
            pg.draw.polygon(surf, self.nh_color, self.vs, 0)
            # disable flag every iteration
            self.is_nh = False
        # if cell in layer state, use special background color
        elif self.is_dir_a:
            pg.draw.polygon(surf, self.dir_a_color, self.vs, 0)
            self.is_dir_a = False
        elif self.is_layer:
            pg.draw.polygon(surf, self.layer_color, self.vs, 0)
            # disable flag every iteration
            self.is_layer = False
        # if cell in horizontal state, use special background color
        elif self.is_horizontal:
            pg.draw.polygon(surf, self.horizontal_color, self.vs, 0)
            # disable flag every iteration
            self.is_horizontal = False
        # if cell in vertical state, use special background color
        elif self.is_vertical:
            pg.draw.polygon(surf, self.vertical_color, self.vs, 0)
            # disable flag every iteration
            self.is_vertical = False
        # draw cell border - always
        pg.draw.polygon(surf, self.border_color, self.vs, self.border_thickness)
    
    # function of setting vertices by current center and outer radius position
    def set_vs(self):
        for i in range(N_SIDES):
            self.vs[i] = self.center + pg.Vector2((m.cos(m.radians(60 * i)), -m.sin(m.radians(60 * i)))) * self.r_out
            self.vs[i] = pg.Vector2(int(self.vs[i].x), int(self.vs[i].y))
    
    # function of printing neighbours
    def print_nhs(self):
        print("\n".join([str(nh) for nh in self.nhs]))

    # function, return string of cell coordinates
    def __str__(self):
        return f"Cell: l = {self.l}; a = {self.a}; s = {self.s}."

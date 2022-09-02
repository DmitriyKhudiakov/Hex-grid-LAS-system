import pygame as pg
import math as m
from Cell import Cell

# angles of polygon - always 6
N_ANGLES = 6


class Grid:
    def __init__(self, n_layers, center, r_out):
        # number of additional levels - always more than zero
        self.n_layers = n_layers
        # position of center of grid
        self.center = center
        # outer radius of cell
        self.r_out = r_out
        # init list of cells (first - center cell is defined here)
        self.grid = [[[Cell(0, 0, 0)]]]
        # fill grid cell list whit cells
        self.fill_grid()
        # connection cells together, set neighbours
        self.linking_cells()
        self.set_geometry()
        # set some interface variables
        self.is_inside_show = False
        self.is_layer_show = False
        self.is_neighbors_show = False
        self.is_horizontal_show = False
        self.is_vertical_show = False
        self.is_dir_a_list = [False for _ in range(6)]
    
    # generator for iterate over all сells, example of usage:
    # for cell in grid.grid_range():
    #   print(cell.some_value)
    def grid_range(self):
        yield self.grid[0][0][0]
        l = 1
        while l < self.n_layers + 1:
            a = 0
            while a < N_ANGLES:
                s = 0
                while s < l:
                    yield self.grid[l][a][s]
                    s += 1
                a += 1
            l += 1
    
    # function set geometry to every cell
    def set_geometry(self):
        # set start cell
        # center of first cell - center of board
        self.grid[0][0][0].center = pg.Vector2(self.center)
        # set outer radius
        self.grid[0][0][0].r_out = self.r_out
        # set vertices
        self.grid[0][0][0].set_vs()
        # set inner radius
        self.grid[0][0][0].r_in = self.r_out * m.cos(m.radians(30))
        
        # two stages of setting geometry:
        # 1) set geometry for cell on main angles axes
        # 2) set geometry for another cells (according to the diagram)
        # set angles lines
        for l in range(1, self.n_layers + 1):
            for a in range(N_ANGLES):
                if l == 1:
                    self.grid[l][a][0].r_out = self.r_out
                    self.grid[l][a][0].r_in = self.r_out * m.cos(m.radians(30))
                    self.grid[l][a][0].center = self.grid[l - 1][0][0].center + 2 * self.grid[l][0][0].r_in \
                                                * pg.Vector2(m.cos(m.radians(30 + a * 60)), -m.sin(m.radians(30 + a * 60)))
                    self.grid[l][a][0].set_vs()
                else:
                    self.grid[l][a][0].r_out = self.r_out
                    self.grid[l][a][0].r_in = self.r_out * m.cos(m.radians(30))
                    self.grid[l][a][0].center = self.grid[l - 1][a][0].center + 2 * self.grid[l][a][0].r_in \
                                                * pg.Vector2(m.cos(m.radians(30 + a * 60)), -m.sin(m.radians(30 + a * 60)))
                    self.grid[l][a][0].set_vs()
        
        # set insides cells
        if self.n_layers > 1:
            for l in range(1, self.n_layers + 1):
                for a in range(N_ANGLES):
                    for s in range(1, l):
                        self.grid[l][a][s].r_out = self.r_out
                        self.grid[l][a][s].r_in = self.r_out * m.cos(m.radians(30))
                        self.grid[l][a][s].center = self.grid[l][a][s - 1].center + 2 * self.grid[l][a][s].r_in \
                                                * pg.Vector2(m.cos(m.radians(30 + a * 60 + 120)), -m.sin(m.radians(30 + a * 60 + 120)))
                        self.grid[l][a][s].set_vs()
        
    # function connects cells together, (define neighbours), connection according to the diagram
    def linking_cells(self):
        
        # linking start cell
        for index, nh in enumerate(self.grid[0][0][0].nhs):
            self.grid[0][0][0].nhs[index] = self.grid[1][index][0]
        
        # linking angles lines
        s = 0
        for l in range(1, self.n_layers + 1):
            for a in range(N_ANGLES):
                ac = self.grid[l][a][s].a
                cc = self.grid[l][a][s]
                
                # 1
                if l == self.n_layers:
                    cc.nhs[ac] = None
                else:
                    cc.nhs[ac] = self.grid[l + 1][ac][s]
                
                # 2
                if l == self.n_layers:
                    cc.nhs[(ac + 1) % 6] = None
                    cc.nhs[(ac + 1) % 6] = None
                else:
                    cc.nhs[(ac + 1) % 6] = self.grid[l + 1][ac][1]
                    cc.nhs[(ac - 1) % 6] = self.grid[l + 1][(ac - 1) % 6][l]
                
                # 3
                if l == 1:
                    cc.nhs[(ac + 3) % 6] = self.grid[0][0][0]
                else:
                    cc.nhs[(ac + 3) % 6] = self.grid[l - 1][ac][0]
                
                # 4
                if l == 1:
                    cc.nhs[(ac + 2) % 6] = self.grid[l][(ac + 1) % 6][0]
                    cc.nhs[(ac - 2) % 6] = self.grid[l][(ac - 1) % 6][0]
                else:
                    cc.nhs[(ac + 2) % 6] = self.grid[l][ac][1]
                    cc.nhs[(ac - 2) % 6] = self.grid[l][(ac - 1) % 6][l - 1]
        
        # linking insides cells
        for l in range(2, self.n_layers + 1):
            for a in range(N_ANGLES):
                for s in range(1, l):
                    ac = self.grid[l][a][s].a
                    cc = self.grid[l][a][s]
                    
                    # 1
                    if l == self.n_layers:
                        cc.nhs[ac] = None
                    else:
                        cc.nhs[ac] = self.grid[l + 1][ac][s]
                    
                    # 2
                    if l == self.n_layers:
                        cc.nhs[(ac + 1) % 6] = None
                    else:
                        cc.nhs[(ac + 1) % 6] = self.grid[l + 1][ac][s + 1]
                    
                    # 3
                    if s == l - 1:
                        cc.nhs[(ac + 2) % 6] = self.grid[l][(ac + 1) % 6][0]
                    else:
                        cc.nhs[(ac + 2) % 6] = self.grid[l][ac][s + 1]
                    
                    # 4
                    if s == l - 1:
                        cc.nhs[(ac + 3) % 6] = self.grid[l - 1][(ac + 1) % 6][0]
                    else:
                        cc.nhs[(ac + 3) % 6] = self.grid[l - 1][ac][s]
                    
                    # 5
                    if s == 1:
                        cc.nhs[(ac - 2) % 6] = self.grid[l - 1][ac][0]
                    else:
                        cc.nhs[(ac - 2) % 6] = self.grid[l - 1][ac][s - 1]
                    
                    # 6
                    cc.nhs[(ac - 1) % 6] = self.grid[l][ac][s - 1]

    # init cell list by appending cells
    def fill_grid(self):
        # cycle through levels
        for curr_layer in range(1, self.n_layers + 1):
            # new empty list of every layer to appending in cells grid list - l coordinate
            curr_layer_list = []
            # cycle through angles
            for curr_angle in range(N_ANGLES):
                # new empty list of every angle to appending in cells grid list - a coordinate
                curr_angle_list = []
                # cycle through steps
                for curr_step in range(curr_layer):
                    # append new Cell with l, a, s coordinates
                    curr_angle_list.append(Cell(curr_layer, curr_angle, curr_step))
                # append angle list to layer list
                curr_layer_list.append(curr_angle_list)
            # append layer list to grid cell list
            self.grid.append(curr_layer_list)
    
    # function return string with grid structure
    def __str__(self):
        return "\n".join([ret_cell_str.__str__() for ret_cell_str in list(Grid.flatten(self.grid, 3))])
    
    # help function to __str__ method
    @staticmethod
    def flatten(value, depth):
        if depth and isinstance(value, list):
            for v in value: yield from Grid.flatten(v, depth - 1)
        else: yield value

    # function handles interface events
    def event_handler(self, events, mouse_pos, keys_pressed, mouse_pressed):
        # some init variables
        curr_layer = None
        curr_cell = None
        
        # check if key is pressed, to show cells with same flag
        keys_pressed = pg.key.get_pressed()
        if keys_pressed[pg.K_i]:
            self.is_inside_show = True
        if keys_pressed[pg.K_l]:
            self.is_layer_show = True
        if keys_pressed[pg.K_n]:
            self.is_neighbors_show = True
        if keys_pressed[pg.K_h]:
            self.is_horizontal_show = True
        if keys_pressed[pg.K_v]:
            self.is_vertical_show = True
        for i, is_dir_a in enumerate(self.is_dir_a_list):
            if keys_pressed[pg.K_a] and keys_pressed[49 + i]:
                self.is_dir_a_list[i] = True
            
        # detect focus cell
        for cell in self.grid_range():
            if cell.is_point_inside(mouse_pos):
                curr_cell = cell
                curr_layer = cell.l
        
        # set flags
        if curr_cell is not None:
            for i, is_dir_list in enumerate(self.is_dir_a_list):
                if is_dir_list:
                    # two ndirections, while cycles
                    curr_a_cell = curr_cell
                    while True:
                        curr_a_cell.is_dir_a = True
                        curr_a_cell = curr_a_cell.nhs[i]
                        if curr_a_cell is None:
                            break
            for cell in self.grid_range():
                # set is_inside flag
                if self.is_inside_show:
                    # detect condition
                    if cell == curr_cell:
                        cell.is_inside = True
                # set is_nh flag
                if self.is_neighbors_show:
                    # detect conditions
                    if cell in curr_cell.nhs:
                        cell.is_nh = True
                # set is_layer flag
                if self.is_layer_show:
                    # detect conditions
                    if cell.l == curr_layer:
                        cell.is_layer = True
                # set is_layer flag
                if self.is_horizontal_show:
                    # detect conditions
                    if cell.l == curr_layer:
                        cell.is_layer = True

    # function draw grid (every cell)
    def draw(self, surf):
        for cell in self.grid_range():
            # dont remember why this condition
            if not (None in cell.vs):
                cell.draw(surf)

import pygame as pg
from Game import Game
from Grid import Grid
from NamedButton import NamedButton
from LineArrow import LineArrow


def test_001():
    game = Game()
    game = Game(fps=60, is_full_screen=False, width=700, height=700)
    # init modules
    grid = Grid(n_layers=4, center=pg.Vector2(200, 350), r_out=25)
    named_button_1 = NamedButton(pos=pg.Vector2(425, 25), width=230, name="Current", font_pixel_size=40, associated_flag=[grid, "is_inside_show"])
    named_button_2 = NamedButton(pos=pg.Vector2(425, 75), width=230, name="Layer", font_pixel_size=40, associated_flag=[grid, "is_layer_show"])
    named_button_3 = NamedButton(pos=pg.Vector2(425, 125), width=230, name="Neighbors", font_pixel_size=40, associated_flag=[grid, "is_neighbors_show"])
    named_button_4 = NamedButton(pos=pg.Vector2(425, 175), width=230, name="Direction A0", font_pixel_size=40, associated_flag=[grid, "is_dir_a_list", 0])
    named_button_5 = NamedButton(pos=pg.Vector2(425, 225), width=230, name="Direction A1", font_pixel_size=40, associated_flag=[grid, "is_dir_a_list", 1])
    named_button_6 = NamedButton(pos=pg.Vector2(425, 275), width=230, name="Direction A2", font_pixel_size=40, associated_flag=[grid, "is_dir_a_list", 2])
    named_button_7 = NamedButton(pos=pg.Vector2(425, 325), width=230, name="Direction A3", font_pixel_size=40, associated_flag=[grid, "is_dir_a_list", 3])
    named_button_8 = NamedButton(pos=pg.Vector2(425, 375), width=230, name="Direction A4", font_pixel_size=40, associated_flag=[grid, "is_dir_a_list", 4])
    named_button_9 = NamedButton(pos=pg.Vector2(425, 425), width=230, name="Direction A5", font_pixel_size=40, associated_flag=[grid, "is_dir_a_list", 5])
    line_arrow = LineArrow(pos=pg.Vector2(175, 600), size=50, line_length=300)
    # set modules
    game.modules.append(grid)
    game.modules.append(named_button_1)
    game.modules.append(named_button_2)
    game.modules.append(named_button_3)
    game.modules.append(named_button_4)
    game.modules.append(named_button_5)
    game.modules.append(named_button_6)
    game.modules.append(named_button_7)
    game.modules.append(named_button_8)
    game.modules.append(named_button_9)
    game.modules.append(line_arrow)
    
    # set special arrow module
    game.arrow = line_arrow
    
    game.main_loop()


def main():
    test_001()


if __name__ == "__main__":
    main()

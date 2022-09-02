import pygame as pg
import sys


# class of game
class Game:
    def __init__(self, fps=60, is_full_screen=False, width=1280, height=720):
        pg.init()
        # init main window size variables
        if is_full_screen:
            self.width = pg.display.Info().current_w
            self.height = pg.display.Info().current_h
            self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN | pg.NOFRAME | pg.DOUBLEBUF | pg.HWSURFACE)
        else:
            self.width = width
            self.height = height
            self.screen = pg.display.set_mode((self.width, self.height),  pg.DOUBLEBUF | pg.HWSURFACE)
        self.screen.convert_alpha()
        self.screen.set_alpha(255)
        
        # default background color
        self.background_color = (30, 30, 30)
        
        # main clock
        self.clock = pg.time.Clock()
        self.fps = fps
        
        # main font settings
        pg.font.init()
        self.font = pg.font.SysFont("Arial", 25)
        self.font_color = (235, 180, 100)
        
        # list of module objects
        self.modules = []
        
        # special module arrow
        # add not_click_detect_flag
        self.arrow = None
        
    # function draw amd blit main information
    def show_work_info(self):
        fps = self.clock.get_fps()
        try:
            fps = int(fps)
        except OverflowError:
            fps = str(fps)
        text_surface_1 = self.font.render(f"fps:{fps}", True, self.font_color)
        text_surface_2 = self.font.render(f"width:{self.width}", True, self.font_color)
        text_surface_3 = self.font.render(f"height:{self.height}", True, self.font_color)
        
        pos_1 = (10, 0)
        pos_2 = (10, text_surface_1.get_height() + 5)
        pos_3 = (10, (text_surface_1.get_height() + 5) * 2)
        
        self.screen.blit(text_surface_1, pos_1)
        self.screen.blit(text_surface_2, pos_2)
        self.screen.blit(text_surface_3, pos_3)
    
    # function handle user events (call module handlers)
    def event_handler(self, events, mouse_pos, keys_pressed, mouse_pressed):
        # handle main close events
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
        for module in self.modules:
            module.event_handler(events, mouse_pos, keys_pressed, mouse_pressed)

    # function check arrow flags
    def get_mouse_pos(self):
        mouse_pos = pg.mouse.get_pos()
        if self.arrow is not None:
            if self.arrow.is_locked:
                return mouse_pos + self.arrow.delta_arrow
        return mouse_pos

    # function draws all module objects (call draw methods)
    def draw_proc(self):
        self.screen.fill(self.background_color)
        for module in self.modules:
            module.draw(self.screen)
        self.show_work_info()
        
    # main loop of game
    def main_loop(self):
        # start fill screen
        self.screen.fill((self.background_color))
        while True:
            # check clock fps
            self.clock.tick(self.fps)
            # get inputs and handle it
            events = pg.event.get()
            mouse_pos = self.get_mouse_pos();
            keys_pressed = pg.key.get_pressed()
            mouse_pressed = pg.mouse.get_pressed()
            self.event_handler(events, mouse_pos, keys_pressed, mouse_pressed)
            # draw process
            self.draw_proc()
            # update whole screen
            pg.display.update()


def main():
    game = Game(fps=60, is_full_screen=True)
    game.main_loop()


if __name__ == "__main__":
    main()
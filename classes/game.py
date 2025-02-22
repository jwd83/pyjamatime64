from pyray import *
import time


class Game:
    def __init__(self):
        self.fps = 0.0
        self.fps_update = 200
        self.frame = 0
        self.time_start = time.time()
        self.last_frame = time.time()
        self.height = 360
        self.width = 640
        self.dt = 1 / 60

    def draw_fps(self):
        draw_text(f"{int(self.fps)} FPS", 10, 10, 30, VIOLET)

    def update_fps(self):
        self.frame += 1
        if self.frame % self.fps_update == 0:
            self.time_end = time.time()
            self.fps = self.fps_update / (self.time_end - self.time_start)
            self.time_start = self.time_end

    def run(self):
        init_window(self.width, self.height, "Hello")
        while not window_should_close():

            # Check for fullscreen toggle
            if is_key_pressed(KeyboardKey.KEY_F11) or is_key_pressed(KeyboardKey.KEY_F):
                toggle_fullscreen()

            begin_drawing()
            clear_background(WHITE)

            # frame complete
            self.draw_fps()
            end_drawing()

            self.update_dt()
            self.update_fps()

        close_window()

    def update_dt(self):
        new_time = time.time()
        self.dt = new_time - self.last_frame
        self.last_frame = new_time

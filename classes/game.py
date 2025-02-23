from pyray import *
from raylib import *
import time


class Game:
    def __init__(self):
        self.fps = 0.0
        self.fps_update = 200
        self.frame = 0
        self.time_start = time.time()
        self.last_frame = time.time()
        self.height = 720
        self.width = 1280
        self.dt = 1 / 60
        self.camera = Camera3D()
        self.camera.position = Vector3(0.0, 10.0, 10.0)
        self.camera.target = Vector3()
        self.camera.up = Vector3(0.0, 1.0, 0.0)
        self.camera.fovy = 45.0
        self.camera.projection = CAMERA_PERSPECTIVE

    def draw_fps(self):
        draw_text(f"{int(self.fps)} FPS", 10, 10, 30, VIOLET)

    def update_fps(self):
        self.frame += 1
        if self.frame % self.fps_update == 0:
            self.time_end = time.time()
            self.fps = self.fps_update / (self.time_end - self.time_start)
            self.time_start = self.time_end

    def start_frame(self):

        # start new frame
        begin_drawing()
        clear_background(WHITE)

    def render_frame_3d(self):
        # 3D
        begin_mode_3d(self.camera)
        draw_grid(10, 1.0)
        end_mode_3d()

    def end_frame(self):

        # frame complete
        self.draw_fps()
        end_drawing()

        # update time for next frame
        self.update_dt()
        self.update_fps()

    def run(self):
        init_window(self.width, self.height, "Hello")
        while not window_should_close():

            # Check for fullscreen toggle
            if is_key_pressed(KeyboardKey.KEY_F11) or is_key_pressed(KeyboardKey.KEY_F):
                # toggle_fullscreen()
                toggle_borderless_windowed()

            self.start_frame()
            self.render_frame_3d()
            self.end_frame()

        close_window()

    def update_dt(self):
        new_time = time.time()
        self.dt = new_time - self.last_frame
        self.last_frame = new_time

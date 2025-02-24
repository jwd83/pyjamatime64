from pyray import *
from raylib import *
import time
from scenes import *


class Game:

    def __init__(self):
        print(f"Game class initialized")
        self.scenes = []
        self.fps = 0.0
        self.fps_update = 200
        self.frame = 0
        self.time_start = time.time()
        self.last_frame = time.time()
        self.height = 720
        self.width = 1280
        self.dt = 1 / 60
        self.mesh_loaded = False
        self.prepare_window()
        self.scenes.append(CubeDemo(self))
        # self.ship = load_model(os.path.join("models", "ship.glb"))
        # self.ship_position = Vector3(0, 0, 5)

    def prepare_window(self):
        self.camera = Camera3D()
        self.camera.position = Vector3(0.0, 10.0, 10.0)
        self.camera.target = Vector3()
        self.camera.up = Vector3(0.0, 1.0, 0.0)
        self.camera.fovy = 45.0
        self.camera.projection = CAMERA_PERSPECTIVE
        self.background_color: Color = BLACK
        init_window(self.width, self.height, "PyjamaTime64")
        self.blank_frame()

    def blank_frame(self):
        begin_drawing()
        clear_background(self.background_color)
        begin_mode_3d(self.camera)
        end_mode_3d()
        end_drawing()

    def draw_fps(self):
        draw_text(f"{int(self.fps)} FPS", 10, 10, 30, VIOLET)

    def update_fps(self):
        self.frame += 1
        if self.frame % self.fps_update == 0:
            self.time_end = time.time()
            self.fps = self.fps_update / (self.time_end - self.time_start)
            self.time_start = self.time_end

    # def render_frame_3d(self):
    # start 3D

    # # move the ship around the origin
    # self.ship_position.x = math.sin(time.time()) * 5
    # self.ship_position.z = math.cos(time.time()) * 5

    # # repoint the ship at the origin
    # self.ship.transform = MatrixRotateXYZ(Vector3(0, time.time(), 0))

    # # draw the ship
    # draw_model(self.ship, self.ship_position, 1.0, WHITE)

    # draw_grid(10, 1.0)

    # draw model
    # draw_model(self.model, self.model_position, 1.0, WHITE)

    # finish 3d
    # end_mode_3d()

    def end_frame(self):

        # frame complete
        self.draw_fps()
        end_drawing()

        # update time for next frame
        self.update_dt()
        self.update_fps()

    def get_input(self):
        # Check for fullscreen toggle
        if is_key_pressed(KeyboardKey.KEY_F11) or is_key_pressed(KeyboardKey.KEY_F):
            # toggle_fullscreen()
            toggle_borderless_windowed()

    def scenes_update(self):
        for scene in self.scenes:
            scene.update()

    def scenes_draw_3d(self):
        for scene in self.scenes:
            scene.draw_3d()

    def scenes_draw_2d(self):
        for scene in self.scenes:
            scene.draw_2d()

    def run(self):
        # toggle_borderless_windowed()

        while not window_should_close():

            # process game-wide input
            self.get_input()

            # have all scenes process their updates
            self.scenes_update()

            # start new frame
            begin_drawing()
            clear_background(self.background_color)

            begin_mode_3d(self.camera)
            self.scenes_draw_3d()
            end_mode_3d()

            self.scenes_draw_2d()
            self.end_frame()

        close_window()

    def update_dt(self):
        new_time = time.time()
        self.dt = new_time - self.last_frame
        self.last_frame = new_time

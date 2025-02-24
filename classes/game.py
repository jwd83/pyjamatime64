import pyray as pr
import raylib as rl
from pyray import *
from raylib import *
import time
from .renderobject import RenderObject
import random
import math
import os


class Game:

    def __init__(self):
        print(f"Game class initialized")
        self.fps = 0.0
        self.fps_update = 200
        self.frame = 0
        self.time_start = time.time()
        self.last_frame = time.time()
        self.height = 720
        self.width = 1280
        self.dt = 1 / 60
        self.mesh_loaded = False
        self.models: list[RenderObject] = []
        self.prepare_window()
        self.ship = load_model(os.path.join("models", "ship.glb"))
        self.ship_position = Vector3(0, 0, 5)

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

    def start_frame(self):

        # start new frame
        begin_drawing()
        clear_background(self.background_color)

    def create_render_object(self):
        pos_range = 4
        cube_size = 0.5
        x = random.randint(-pos_range, pos_range)
        y = random.randint(-pos_range, pos_range)
        z = random.randint(-pos_range, pos_range)
        color = random.choice(
            [
                RED,
                GREEN,
                BLUE,
                YELLOW,
                ORANGE,
                PURPLE,
                PINK,
                BROWN,
                SKYBLUE,
                LIME,
                GOLD,
                MAROON,
            ]
        )
        mesh = gen_mesh_cube(cube_size, cube_size, cube_size)
        model = load_model_from_mesh(mesh)
        model_position = Vector3(x, y, z)
        self.models.append(RenderObject(model, model_position, 1.0, color))

    def render_frame_3d(self):
        # start 3D

        # rotate camera around the origin by time
        self.camera.position.x = math.sin(time.time()) * 10
        self.camera.position.z = math.cos(time.time()) * 10

        # move the camera up and down vertical as well
        self.camera.position.y = math.sin(time.time() * 0.5) * 10

        begin_mode_3d(self.camera)

        if not self.mesh_loaded:
            self.mesh_loaded = True
            for j in range(400):

                self.create_render_object()

        for model in self.models:
            model.draw()

        # move the ship around the origin
        self.ship_position.x = math.sin(time.time()) * 5
        self.ship_position.z = math.cos(time.time()) * 5

        # repoint the ship at the origin
        self.ship.transform = MatrixRotateXYZ(Vector3(0, time.time(), 0))

        # draw the ship
        draw_model(self.ship, self.ship_position, 1.0, WHITE)

        # draw_grid(10, 1.0)

        # draw model
        # draw_model(self.model, self.model_position, 1.0, WHITE)

        # finish 3d
        end_mode_3d()

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

    def run(self):
        # toggle_borderless_windowed()

        while not window_should_close():

            self.get_input()
            self.start_frame()
            self.render_frame_3d()
            self.end_frame()

            # remove the first model from the list of models and create a new one
            self.models.pop(0)
            self.create_render_object()

        close_window()

    def update_dt(self):
        new_time = time.time()
        self.dt = new_time - self.last_frame
        self.last_frame = new_time

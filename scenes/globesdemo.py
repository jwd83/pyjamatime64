from pt import *
import os
import math
import time


class GlobesDemo(Scene):

    def __init__(self, game):
        super().__init__(game)

        self.min_scale_earth = 0.1
        self.max_scale_cmbr = 4
        self.max_scale_milky_way = 2

        self.earth = load_model(os.path.join("assets", "models", "earth.glb"))
        self.earth_position = Vector3(0, 0, 0)
        self.earth_scale = 5.0
        self.earth_color = WHITE
        self.earth_visible = True

        self.moon = load_model(os.path.join("assets", "models", "moon.glb"))
        self.moon_position = Vector3(0, 0, 0)
        self.moon_scale = 5.0
        self.moon_color = WHITE
        self.moon_visible = True

        self.cmbr = load_model(os.path.join("assets", "models", "cmbr.glb"))
        self.cmbr_position = Vector3(0, 0, 0)
        self.cmbr_scale = 0.1
        self.cmbr_color = Color(255, 255, 255, 16)
        self.cmbr_visible = True

        self.milky_way = load_model(os.path.join("assets", "models", "milky-way.glb"))
        self.milky_way_position = Vector3(0, 0, 0)
        self.milky_way_scale = 0.1
        self.milky_way_color = Color(255, 255, 255, 220)
        self.milky_way_visible = True

        print("GlobesDemo __init__ complete")

    def update_camera(self):

        # rotate camera around the origin by time
        self.camera.position.x = math.sin(time.time()) * 10
        self.camera.position.z = math.cos(time.time()) * 10

        # move the camera up and down vertical as well
        self.camera.position.y = math.sin(time.time() * 0.5) * 10

    def update_inputs(self):

        if is_key_pressed(rl.KEY_E):
            self.earth_visible = not self.earth_visible

        if is_key_pressed(rl.KEY_C):
            self.cmbr_visible = not self.cmbr_visible

        if is_key_pressed(rl.KEY_M):
            self.milky_way_visible = not self.milky_way_visible

        if is_key_pressed(rl.KEY_N):
            self.moon_visible = not self.moon_visible

    def update(self):
        self.update_camera()
        self.update_inputs()

        self.earth_scale = max(self.min_scale_earth, self.earth_scale - self.game.dt)
        self.cmbr_scale = min(self.max_scale_cmbr, self.cmbr_scale + self.game.dt)
        self.milky_way_scale = min(
            self.max_scale_milky_way, self.milky_way_scale + self.game.dt
        )

    def draw_3d(self):
        if self.earth_visible:
            draw_model(
                self.earth, self.earth_position, self.earth_scale, self.earth_color
            )

        if self.moon_visible:
            draw_model(self.moon, self.moon_position, self.moon_scale, self.moon_color)

        if self.milky_way_visible:
            draw_model(
                self.milky_way,
                self.milky_way_position,
                self.milky_way_scale,
                self.milky_way_color,
            )
        if self.cmbr_visible:
            draw_model(self.cmbr, self.cmbr_position, self.cmbr_scale, self.cmbr_color)

    def draw_2d(self):
        pass

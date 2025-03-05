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

        self.cmbr = load_model(os.path.join("assets", "models", "cmbr4.glb"))
        self.cmbr_position = Vector3(0, 0, 0)
        self.cmbr_scale = 0.1
        self.cmbr_color = Color(255, 255, 255, 16)

        self.milky_way = load_model(os.path.join("assets", "models", "milky-way.glb"))
        self.milky_way_position = Vector3(0, 0, 0)
        self.milky_way_scale = 0.1
        self.milky_way_color = Color(255, 255, 255, 220)

        self.draw_cmbr = True
        self.draw_milky_way = True
        self.draw_earth = True

        print("GlobesDemo __init__ complete")

    def update_camera(self):

        # rotate camera around the origin by time
        self.camera.position.x = math.sin(time.time()) * 10
        self.camera.position.z = math.cos(time.time()) * 10

        # move the camera up and down vertical as well
        self.camera.position.y = math.sin(time.time() * 0.5) * 10

    def update_inputs(self):

        if is_key_pressed(rl.KEY_E):
            self.draw_earth = not self.draw_earth

        if is_key_pressed(rl.KEY_C):
            self.draw_cmbr = not self.draw_cmbr

        if is_key_pressed(rl.KEY_M):
            self.draw_milky_way = not self.draw_milky_way

    def update(self):
        self.update_camera()
        self.update_inputs()

        self.earth_scale = max(self.min_scale_earth, self.earth_scale - self.game.dt)
        self.cmbr_scale = min(self.max_scale_cmbr, self.cmbr_scale + self.game.dt)
        self.milky_way_scale = min(
            self.max_scale_milky_way, self.milky_way_scale + self.game.dt
        )

    def draw_3d(self):
        if self.draw_earth:
            draw_model(
                self.earth, self.earth_position, self.earth_scale, self.earth_color
            )

        if self.draw_milky_way:
            draw_model(
                self.milky_way,
                self.milky_way_position,
                self.milky_way_scale,
                self.milky_way_color,
            )
        if self.draw_cmbr:
            draw_model(self.cmbr, self.cmbr_position, self.cmbr_scale, self.cmbr_color)

    def draw_2d(self):
        pass

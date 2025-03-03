from pt import *
import os
import math
import time


class GlobesDemo(Scene):

    def __init__(self, game):
        super().__init__(game)

        self.earth = load_model(os.path.join("models", "earth.glb"))
        self.earth_position = Vector3(0, 0, 0)
        self.earth_scale = 1.0
        self.earth_color = WHITE

        self.cmbr = load_model(os.path.join("models", "cmbr4.glb"))
        self.cmbr_position = Vector3(0, 0, 0)
        self.cmbr_scale = 4.0
        self.cmbr_color = Color(255, 255, 255, 96)

        self.draw_cmbr = True
        self.draw_earth = True

        print("GlobesDemo __init__ complete")

    def update(self):

        # rotate camera around the origin by time
        self.camera.position.x = math.sin(time.time()) * 10
        self.camera.position.z = math.cos(time.time()) * 10

        # move the camera up and down vertical as well
        self.camera.position.y = math.sin(time.time() * 0.5) * 10

        if is_key_pressed(rl.KEY_E):
            self.draw_earth = not self.draw_earth

        if is_key_pressed(rl.KEY_C):
            self.draw_cmbr = not self.draw_cmbr

    def draw_3d(self):
        if self.draw_earth:
            draw_model(
                self.earth, self.earth_position, self.earth_scale, self.earth_color
            )
        if self.draw_cmbr:
            draw_model(self.cmbr, self.cmbr_position, self.cmbr_scale, self.cmbr_color)

    def draw_2d(self):
        pass

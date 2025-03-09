from pt import *
import os
import math
import time


class CMBRDemo(Scene):

    def __init__(self, game):
        super().__init__(game)

        self.cmbr = load_model(os.path.join("assets", "models", "cmbr.glb"))
        self.cmbr_position = Vector3(0, 0, 0)
        self.cmbr_scale = 2.0
        self.cmbr_color = WHITE

        print("CMBRDemo __init__ complete")

    def update(self):

        # rotate camera around the origin by time
        self.camera.position.x = math.sin(time.time()) * 10
        self.camera.position.z = math.cos(time.time()) * 10

        # move the camera up and down vertical as well
        self.camera.position.y = math.sin(time.time() * 0.5) * 10

    def draw_3d(self):
        draw_model(self.cmbr, self.cmbr_position, self.cmbr_scale, self.cmbr_color)

    def draw_2d(self):
        pass

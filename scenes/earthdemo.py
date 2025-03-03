from pt import *
import os
import math
import time


class EarthDemo(Scene):

    def __init__(self, game):
        super().__init__(game)

        self.earth = load_model(os.path.join("models", "earth.glb"))
        self.earth_position = Vector3(0, 0, 0)
        self.earth_scale = 2.0
        self.earth_color = WHITE

        print("EarthDemo __init__ complete")

    def update(self):

        # rotate camera around the origin by time
        self.camera.position.x = math.sin(time.time()) * 10
        self.camera.position.z = math.cos(time.time()) * 10

        # move the camera up and down vertical as well
        self.camera.position.y = math.sin(time.time() * 0.5) * 10

    def draw_3d(self):
        draw_model(self.earth, self.earth_position, self.earth_scale, self.earth_color)

    def draw_2d(self):
        pass

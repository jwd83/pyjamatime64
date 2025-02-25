from pt import *
import math
import time
import os


class ShipDemo(Scene):

    def __init__(self, game):
        super().__init__(game)

        # load the ship model

        # ship_model = load_model("models/ship.glb")
        self.ship = load_model(os.path.join("models", "ship.glb"))
        self.ship_position = Vector3(0, 0, 0)
        self.ship_scale = 1.0
        self.ship_color = WHITE
        # ship_mesh = load_model_from_mesh(ship_model.meshes[0])
        # face the camera at the origin
        self.camera.target = Vector3()  # defaults to 0,0,0

    def update(self):

        # rotate camera around the origin by time
        self.camera.position.x = math.sin(time.time()) * 10
        self.camera.position.z = math.cos(time.time()) * 10

        # move the camera up and down vertical as well
        self.camera.position.y = math.sin(time.time() * 0.5) * 10

    def draw_3d(self):
        draw_model(self.ship, self.ship_position, self.ship_scale, self.ship_color)

    def draw_2d(self):
        pass
